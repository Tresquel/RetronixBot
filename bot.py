import interactions
import json
import os
bot = interactions.Client(token=os.environ["TOKEN"])

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
            type="rich",    
        )
        embed.add_field(
            name="Current owner:",
            value=ItemData[item_id]["current_owner"]
        )
        embed.add_field(
            name="Last sold for:",
            #value is the price with a dollar sign at the end
            value=f"${ItemData[item_id]['price']}"
        )
        embed.add_field(
            name="Last sold on:",
            value=ItemData[item_id]["purchase_date"]
        )
        await ctx.send(embeds=embed)
    else:
        await ctx.send("Item not found")

bot.start()