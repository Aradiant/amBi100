import pygame as pg

# Vertical Slider Class
class VerticalSlider:
    def __init__(self, x, y, height, min_value, max_value, initial_value):
        self.x = x  # X position of the slider
        self.y = y  # Y position of the slider
        self.height = height  # Height of the slider track
        self.min_value = min_value  # Minimum value of the slider
        self.max_value = max_value  # Maximum value of the slider
        self.value = initial_value  # Current value of the slider

        # Slider dimensions
        self.track_width = 10  # Width of the slider track
        self.handle_width = 50  # Width of the slider handle
        self.handle_height = 20  # Height of the slider handle

        # Colors
        self.track_color = (100, 100, 100)  # Color of the slider track
        self.handle_color = (200, 200, 200)  # Color of the slider handle

        # Calculate the handle's initial position
        self.handle_y = self.y + (self.height - self.handle_height) * (
            (self.max_value - self.value) / (self.max_value - self.min_value)
        )

    def draw(self, screen):
        # Draw the slider track
        pg.draw.rect(
            screen,
            self.track_color,
            (self.x - self.track_width // 2, self.y, self.track_width, self.height),
        )

        # Draw the slider handle
        pg.draw.rect(
            screen,
            self.handle_color,
            (
                self.x - self.handle_width // 2,
                self.handle_y,
                self.handle_width,
                self.handle_height,
            ),
        )

    def update(self, mouse_pos, mouse_pressed):
        # Check if the handle is being dragged
        if mouse_pressed[0]:  # Left mouse button is pressed
            handle_rect = pg.Rect(
                self.x - self.handle_width // 2,
                self.handle_y,
                self.handle_width,
                self.handle_height,
            )
            if handle_rect.collidepoint(mouse_pos):
                # Update the handle's position
                self.handle_y = mouse_pos[1] - self.handle_height // 2

                # Clamp the handle's position within the track
                self.handle_y = max(self.y, min(self.handle_y, self.y + self.height - self.handle_height))

                # Calculate the slider's value based on the handle's position
                self.value = self.max_value - (
                    (self.handle_y - self.y) / (self.height - self.handle_height)
                ) * (self.max_value - self.min_value)

    def get_value(self):
        return self.value


# Initialize pg
pg.init()

# Set up the display
screen = pg.display.set_mode((400, 600))
pg.display.set_caption("Vertical Slider Example")

# Create a vertical slider
slider = VerticalSlider(x=200, y=100, height=400, min_value=0, max_value=100, initial_value=50)

# Main loop
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Get mouse position and state
    mouse_pos = pg.mouse.get_pos()
    mouse_pressed = pg.mouse.get_pressed()

    # Update the slider
    slider.update(mouse_pos, mouse_pressed)

    # Fill the screen with a background color
    screen.fill((30, 30, 30))  # Dark gray background

    # Draw the slider
    slider.draw(screen)

    # Display the slider's value
    font = pg.font.Font(None, 36)
    text = font.render(f"Value: {int(slider.get_value())}", True, (255, 255, 255))
    screen.blit(text, (10, 10))

    # Update the display
    pg.display.flip()

# Quit pg
pg.quit()