import logging
import json

from dotenv import load_dotenv
from livekit import rtc
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    cli,
    room_io,
    function_tool,
    RunContext,
)
from livekit.plugins import google, noise_cancellation

logger = logging.getLogger("agent")

load_dotenv(".env.local")

# Hardcoded product catalog
PRODUCT_CATALOG = {
    "categories": [
        {
            "name": "Produce",
            "items": [
                {"id": "P001", "name": "Tomatoes", "price": 2.99, "unit": "lb"},
                {"id": "P002", "name": "Onions", "price": 1.49, "unit": "lb"},
                {"id": "P003", "name": "Garlic", "price": 0.99, "unit": "head"},
                {"id": "P004", "name": "Potatoes", "price": 3.49, "unit": "5lb bag"},
                {"id": "P005", "name": "Carrots", "price": 1.99, "unit": "lb"},
                {"id": "P006", "name": "Bell Peppers", "price": 2.49, "unit": "each"},
                {"id": "P007", "name": "Lettuce", "price": 2.99, "unit": "head"},
                {"id": "P008", "name": "Avocados", "price": 1.50, "unit": "each"},
                {"id": "P009", "name": "Bananas", "price": 0.59, "unit": "lb"},
                {"id": "P010", "name": "Apples", "price": 3.99, "unit": "lb"},
            ],
        },
        {
            "name": "Meat & Seafood",
            "items": [
                {"id": "M001", "name": "Ground Beef", "price": 5.99, "unit": "lb"},
                {"id": "M002", "name": "Chicken Breast", "price": 4.99, "unit": "lb"},
                {"id": "M003", "name": "Bacon", "price": 6.49, "unit": "12oz"},
                {"id": "M004", "name": "Salmon Fillet", "price": 12.99, "unit": "lb"},
                {"id": "M005", "name": "Pork Chops", "price": 4.49, "unit": "lb"},
                {"id": "M006", "name": "Steak", "price": 14.99, "unit": "lb"},
                {"id": "M007", "name": "Ground Turkey", "price": 4.99, "unit": "lb"},
                {"id": "M008", "name": "Shrimp", "price": 9.99, "unit": "lb"},
            ],
        },
        {
            "name": "Dairy & Eggs",
            "items": [
                {"id": "D001", "name": "Milk", "price": 3.49, "unit": "gallon"},
                {"id": "D002", "name": "Eggs", "price": 4.99, "unit": "dozen"},
                {"id": "D003", "name": "Butter", "price": 4.49, "unit": "lb"},
                {"id": "D004", "name": "Cheddar Cheese", "price": 5.99, "unit": "8oz"},
                {"id": "D005", "name": "Yogurt", "price": 0.99, "unit": "cup"},
                {"id": "D006", "name": "Cream Cheese", "price": 3.99, "unit": "8oz"},
                {"id": "D007", "name": "Parmesan", "price": 6.99, "unit": "8oz"},
            ],
        },
        {
            "name": "Bakery",
            "items": [
                {"id": "B001", "name": "Bread", "price": 2.99, "unit": "loaf"},
                {"id": "B002", "name": "Bagels", "price": 4.49, "unit": "6 pack"},
                {"id": "B003", "name": "Croissants", "price": 5.99, "unit": "4 pack"},
                {"id": "B004", "name": "Muffins", "price": 4.99, "unit": "6 pack"},
                {"id": "B005", "name": "Garlic Bread", "price": 3.49, "unit": "loaf"},
            ],
        },
        {
            "name": "Pantry",
            "items": [
                {"id": "T001", "name": "Spaghetti", "price": 1.99, "unit": "16oz"},
                {"id": "T002", "name": "Rice", "price": 2.99, "unit": "2lb"},
                {"id": "T003", "name": "Pasta Sauce", "price": 3.49, "unit": "24oz"},
                {"id": "T004", "name": "Olive Oil", "price": 7.99, "unit": "500ml"},
                {
                    "id": "T005",
                    "name": "Canned Tomatoes",
                    "price": 1.49,
                    "unit": "14oz",
                },
                {"id": "T006", "name": "Black Beans", "price": 1.29, "unit": "15oz"},
                {"id": "T007", "name": "Chicken Broth", "price": 2.49, "unit": "32oz"},
                {"id": "T008", "name": "Cooking Oil", "price": 6.99, "unit": "16oz"},
            ],
        },
        {
            "name": "Frozen",
            "items": [
                {"id": "F001", "name": "Ice Cream", "price": 5.99, "unit": "48oz"},
                {"id": "F002", "name": "Frozen Pizza", "price": 7.99, "unit": "each"},
                {
                    "id": "F003",
                    "name": "Frozen Vegetables",
                    "price": 2.49,
                    "unit": "16oz",
                },
                {"id": "F004", "name": "French Fries", "price": 3.49, "unit": "32oz"},
                {"id": "F005", "name": "Frozen Fruit", "price": 4.99, "unit": "16oz"},
            ],
        },
        {
            "name": "Beverages",
            "items": [
                {"id": "BE001", "name": "Orange Juice", "price": 4.99, "unit": "52oz"},
                {"id": "BE002", "name": "Coffee", "price": 9.99, "unit": "12oz"},
                {"id": "BE003", "name": "Tea", "price": 3.99, "unit": "20 bags"},
                {"id": "BE004", "name": "Soda", "price": 5.99, "unit": "12 pack"},
                {"id": "BE005", "name": "Water", "price": 4.99, "unit": "24 pack"},
            ],
        },
    ]
}


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are Siza, a friendly supermarket shopping assistant. Your role is to help customers with their grocery shopping through natural conversation.

CAPABILITIES:
- Browse and search the product catalog using the available tools
- Add items to shopping cart
- Check prices and product availability
- Create and manage shopping lists
- Process orders
- Arrange pickup or delivery

PERSONALITY:
- Be warm, helpful, and conversational
- Make suggestions based on what they're buying
- Keep responses concise and natural
- Never use complex formatting or emojis
- Talk fast.

SHOPPING FLOW:
1. Greet the customer and ask what they need
2. Search for products they mention using the search_products tool
3. Confirm items and prices before adding to cart
4. Offer suggestions (e.g., "Would you like anything else?")
5. When ready to checkout, summarize the order and ask about pickup/delivery

PICKUP & DELIVERY:
- Pickup: Order ready within 1 hour, customer picks up at store
- Delivery: Same-day delivery available within 5 miles

Always confirm prices and get explicit confirmation before adding items to cart.""",
        )

    @function_tool()
    async def get_product_catalog(self, context: RunContext) -> str:
        """Get the full product catalog with all available items, categories, and prices.

        Use this tool when the customer wants to:
        - See what products are available
        - Browse products by category
        - Search for specific items
        - Check prices of products

        Returns the complete product catalog in JSON format.
        """
        return json.dumps(PRODUCT_CATALOG, indent=2)

    @function_tool()
    async def search_products(self, context: RunContext, query: str) -> str:
        """Search for products in the catalog by name or category.

        Args:
            query: The search term (product name or category)

        Use this tool when the customer is looking for specific items or wants to browse a category.
        """
        results = []
        query_lower = query.lower()

        for category in PRODUCT_CATALOG["categories"]:
            # Check if category matches
            if query_lower in category["name"].lower():
                results.append(category)
            else:
                # Check items in category
                matching_items = [
                    item
                    for item in category["items"]
                    if query_lower in item["name"].lower()
                ]
                if matching_items:
                    results.append({"name": category["name"], "items": matching_items})

        return (
            json.dumps(results, indent=2)
            if results
            else json.dumps({"message": "No products found"})
        )


server = AgentServer()


@server.rtc_session(agent_name="my-agent")
async def my_agent(ctx: JobContext):
    # Logging setup
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    # Use Gemini Realtime model - handles STT, LLM, and TTS in one model
    session = AgentSession(
        llm=google.realtime.RealtimeModel(
            voice="Puck",
            temperature=0.8,
            instructions="You are Siza, a friendly supermarket shopping assistant. Be helpful, concise, and natural in your responses.",
        ),
    )

    # Start the session
    await session.start(
        agent=Assistant(),
        room=ctx.room,
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda params: (
                    noise_cancellation.BVCTelephony()
                    if params.participant.kind
                    == rtc.ParticipantKind.PARTICIPANT_KIND_SIP
                    else noise_cancellation.BVC()
                ),
            ),
        ),
    )

    # Join the room and connect to the user
    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(server)
