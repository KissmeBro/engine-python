
class Help:
    """
    Provides usage instructions and important notes for Google Custom Search API.

    Attributes:
        message (str): Detailed help message including API limits and how to get API Key
                       and CSE ID with official links.
    """

    message = (
        "📌 Important notes about Google Custom Search API usage:\n\n"
        "1️⃣ Request limits:\n"
        "   - Google API usually allows 100 free requests per day.\n"
        "   - Exceeding this causes an 'API quota exceeded' error.\n"
        "   - Upgrade your Google Cloud project to increase quota.\n\n"
        "2️⃣ Obtaining API Key and CSE ID:\n"
        "   - API Key: Get it from Google Cloud Console:\n"
        "     https://developers.google.com/custom-search/v1/introduction\n"
        "   - CSE ID: Create your Custom Search Engine here:\n"
        "     https://programmablesearchengine.google.com/controlpanel/create\n\n"
        "3️⃣ Notes:\n"
        "   - Set API Key and CSE ID correctly in your code.\n"
        "   - Use async for better speed and efficiency.\n"
        "   - Check logs if unexpected errors happen.\n\n"
        "Good luck! 🚀")

    def __str__(self) -> str:
        """
        Return the help message when the Help class is printed.

        Returns:
            str: The detailed help message.
        """
        return self.message


Help = Help()
