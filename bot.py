import time
import interactions
import json
import os
from dotenv import load_dotenv
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


load_dotenv()
bot = interactions.Client(token=os.environ["TOKEN"])

if not os.path.isfile("items.json"):
    with open("items.json", "w") as f:
        json.dump({}, f)

with open("items.json", "r") as read_content:
    ItemData = json.load(read_content)

ids = []
for entry in json.load(open("minecraftitems.json", "r")):
    ids.append(entry["name"])

@bot.event()
async def on_ready():
    print("Bot is ready!")
    await bot.change_presence(interactions.ClientPresence(activities=[interactions.PresenceActivity(name="Retronix Reborn", type=interactions.PresenceActivityType.GAME)]))

@bot.command(
    name="getinfo",
    description="Get Info about an item",
    options = [
        interactions.Option(
            name="item_id",
            description="What item to get info about",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ]
)
async def GetItemInfo(ctx: interactions.CommandContext, item_id: str):
    if(item_id in ItemData):
        embed = interactions.Embed(
            title=ItemData[item_id]["name"],
            image=interactions.EmbedImageStruct(url="https://raw.githubusercontent.com/InventivetalentDev/minecraft-assets/1.19/assets/minecraft/textures/item/" + ItemData[item_id]["id"] + ".png"),
            color=0x00cc22
        )
        embed.add_field(
            name="ID:",
            value=item_id
        )
        embed.add_field(
            name="Description:",
            value=ItemData[item_id]["description"]
        )
        embed.add_field(
            name="Current owner:",
            value=ItemData[item_id]["current_owner"]
        )
        embed.add_field(
            name="Last sold for:",
            value=f"${ItemData[item_id]['price']}"
        )
        embed.add_field(
            name="Last sold on:",
            value=ItemData[item_id]["purchase_date"]
        )
        embed.add_field(
            name="How many are there and which one is it:",
            value=ItemData[item_id]["serialnumber"]
        )
        await ctx.send(embeds=embed)
    else:
        embed = interactions.Embed(
            title="Item not found",
            color=0xff1919
        )
        embed.add_field(
            name="Hmm, I can't find that item",
            value="I can't seem to find the item you requested.\nPlease make sure the ID you entered is correct."
        )
        await ctx.send(embeds=embed)

@bot.command(
    name="createitems",
    description="Create items",
    default_member_permissions=interactions.Permissions.ADMINISTRATOR,
    options = [
        interactions.Option(
            name="item_id",
            description="Minecrat item ID",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="item_name",
            description="Item name",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="item_description",
            description="Item description",
            type=interactions.OptionType.STRING,
            required=True,
        ),
        interactions.Option(
            name="item_price",
            description="Item price",
            type=interactions.OptionType.INTEGER,
            required=True,
        ),
        interactions.Option(
            name="count",
            description="How many items to create",
            type=interactions.OptionType.INTEGER,
            required=True,
        ),
    ],
)
async def CreateItems(ctx: interactions.CommandContext, item_id: str, item_name: str, item_description: str, item_price: int, count: int):
    if(item_id in ids):
        lowername = item_name.replace(" ", "_").lower()
        for i in range(count):
            ItemData[lowername + str(i)] = {
                "name": item_name,
                "description": item_description,
                "id": item_id,
                "current_owner": "Nobody",
                "price": item_price,
                "purchase_date": f"<t:{str(int(round(time.time())))}:d>",
                "serialnumber": f"{str(i)}/{str(count)}"
            }
        with open("items.json", "w") as write_content:
            json.dump(ItemData, write_content, indent=4)
        embed = interactions.Embed(
            title="Success!",
            color=0x00cc22
        )
        string = ""
        for i in range(count):
            string += f"{lowername}{i}\n"
        embed.add_field(
            name="Items created:",
            value=string
        )
        await ctx.send(embeds=embed)
    else:
        embed = interactions.Embed(
            title="Incorrect Item",
            color=0xff1919
        )
        embed.add_field(
            name="Not a valid minecraft item.",
            value="The minecraft item ID you entered is not valid.\nPlease make sure the ID you entered is correct."
        )
        embed.add_field(
            name="Examples of bad IDs",
            value="stnoe - spelling error\ndiamond sword - spaces arent allowed: diamond_sword\nminecraft:diamond_sword - 'minecraft:' isnt needed, just the item name"
        )
        await ctx.send(embeds=embed)
bot.start()