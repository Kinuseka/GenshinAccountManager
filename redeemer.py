from manager import Load_accounts, CacheStore
from loguru import logger
import genshin
import asyncio
__version__ = "0.0.1"

async def set_hoyolab(username, password):
    cli = genshin.Client(game=genshin.Game.GENSHIN)
    cache_store = CacheStore(username+"_hoyolab")
    loaded = cache_store.load()
    if loaded:
        cli.set_cookies(loaded)
    else:
        cookies = await cli.login_with_app_password(account=username, password=password)
        cli.set_cookies(cookies.dict())
    cache_store.dump(cookies.dict())
    return cli

async def validate_cookies(client: genshin.Client):
    "Runs one authenticated request to test if the cookies are still valid"
    try:
        await client.get_game_accounts()
    except genshin.errors.InvalidCookies:
        return False
    return True

async def set_client(username, password, attempts=0, nocookies=False):
    if attempts >= 5:
        raise TimeoutError(f"Cannot login to {username} account")
    cli = genshin.Client(game=genshin.Game.GENSHIN)
    cache_store = CacheStore(username)
    loaded = cache_store.load()
    if loaded and not nocookies:
        cli.set_cookies(loaded)
    else:
        cookies = await cli.login_with_password(account=username, password=password)
        cli.set_cookies(cookies.model_dump())
        cache_store.dump(cookies.model_dump())
    if not await validate_cookies(cli):
        cli = await set_client(username=username, password=password, attempts=attempts+1, nocookies=True)
    return cli

async def claim_daily(client: genshin.Client):
    try:
        resp = await client.claim_daily_reward()
        print(f"Got: {resp.name}, Value: {resp.amount}")
    except genshin.errors.AlreadyClaimed:
        print("Daily already claimed!")
        return False
    return True

async def redeem(client: genshin.Client, code: str, game = genshin.Game.GENSHIN):
    """
    Redeem a code to your preferred game

    client: Already logged in client
    code: Valid redeemable code
    game: Game type
    """
    linked_games = await client.get_game_accounts()
    print(f"Found {len(linked_games)} linked game accounts")
    for each_game in linked_games:
        print(f'Trying: {each_game.uid}')
        if each_game.game != game:
            print(f"Game not {game}, skipped")
            continue
        try:
            resp = await client.redeem_code(code=code, uid=each_game.uid)
        except genshin.errors.RedemptionException as e:
            print(f'>> Cannot redeem for this game: {e}')
            return False
        except genshin.errors.InvalidCookies as e:
            print("Failed to login invalid cookies")
            return False
        print(">> No error occured, Success..? ")
        return True

async def main(code):
    accounts = Load_accounts()
    for each in accounts:
        client = await set_client(username=each.username, password=each.password)
        print(f"Logged in {each.username} and ready to redeem at: {client.game}")
        if code:
            result = await redeem(client=client, code=code)
        print("Claiming dailies to hoyolab")
        await claim_daily(client=client)

def menu():
    print(f"Hoyoverse Account manager: {__version__}")
    user_input = input("Enter code (empty to claim only dailies):").strip()
    return user_input

if __name__ == "__main__":
    code = menu()
    asyncio.run(main(code=code))
