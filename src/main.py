import sys

from app.app import App


# Create App Object
app: App = App()

# Run App(loop forever)
app.start()

# Exit Program
sys.exit()
