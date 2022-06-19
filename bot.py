import interactions
import json
import os
bot = interactions.Client(token=os.environ["TOKEN"])

if not os.path.isfile("items.json"):
    with open("items.json", "w") as f:
        json.dump({}, f)

with open("items.json", "r") as read_content:
    ItemData = json.load(read_content)

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

bot.start()