import arcade

# Constants
SCREEN_WIDTH = 1248
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Jump It"

# Constants used to scale our sprites from their original size
TILE_SCALING = 1
CHARACTER_SCALING = TILE_SCALING
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 10
GRAVITY = 1.4
PLAYER_JUMP_SPEED = 25


PLAYER_START_X = 2
PLAYER_START_Y = 1

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_BACKGROUND = "Background"
LAYER_NAME_PLAYER = "Player"
LAYER_NAME_SPIKE = "Spike"
LAYER_NAME_DUCK = "Duck"


def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]


class Entity(arcade.Sprite):
    def __init__(self, name_folder, name_file):
        super().__init__()

        # Default to facing right
        self.facing_direction = RIGHT_FACING

        # Used for image sequences
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING

        self.idle_texture_pair = load_texture_pair("assets/Base_Model.png")
        self.jump_texture_pair = load_texture_pair("assets/Jump.png")

        # Load textures for walking
        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair("assets/Walk.png")
            self.walk_textures.append(texture)

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        self.set_hit_box(self.texture.hit_box_points)


class PlayerCharacter(Entity):
    """Player Sprite"""

    def __init__(self):

        # Set up parent class
        super().__init__("stickman", "stickman")

        # Track our state
        self.jumping = False

    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.facing_direction == RIGHT_FACING:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == LEFT_FACING:
            self.facing_direction = RIGHT_FACING

        # Jumping animation
        if self.change_y > 0:
            self.texture = self.jump_texture_pair[self.facing_direction]
            return
        elif self.change_y < 0:
            self.texture = self.jump_texture_pair[self.facing_direction]
            return

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.facing_direction]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 7:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture][self.facing_direction]


class MyGame(arcade.Window):
    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.jump_needs_reset = False
        self.reset_pressed = False

        # Our TileMap Object
        self.tile_map = None

        # Our Scene Object
        self.scene = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our 'physics' engine
        self.physics_engine = None


        self.end_of_map = 0

        # Keep track of the score
        self.score = 1000

        self.win_text = ""
        self.final_score = ""
        self.reset_text = ""

        # Load sounds
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")
        self.win = arcade.load_sound(":resources:sounds/upgrade1.wav")


    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # Map name
        map_name = "assets/MapFinal.JSON"

        # Layer Specific Options for the Tilemap
        layer_options = {
            LAYER_NAME_PLATFORMS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_SPIKE: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_DUCK: {
                "use_spatial_hash": True,
            },
        }

        # Load in TileMap and set as scene
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options, None, "Simple", 4.5, (-48,0))
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Set up the player, specifically placing it at these coordinates.
        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_x = (self.tile_map.tile_width * TILE_SCALING * PLAYER_START_X)
        self.player_sprite.center_y = (self.tile_map.tile_height * TILE_SCALING * PLAYER_START_Y)
        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)

        # Calculate the right edge of the my_map in pixels
        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            gravity_constant=GRAVITY,
            walls=self.scene[LAYER_NAME_PLATFORMS]
        )

        self.win_text = ""
        self.final_score = ""
        self.reset_text = ""

    def restart(self):
        # Set up the player, specifically placing it at these coordinates.
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0
        self.jump_needs_reset = False
        self.right_pressed = False
        self.left_pressed = False
        self.player_sprite.center_x = (self.tile_map.tile_width * TILE_SCALING * PLAYER_START_X)
        self.player_sprite.center_y = (self.tile_map.tile_height * TILE_SCALING * PLAYER_START_Y)

    def on_draw(self):
        # Clear the screen to the background color
        self.clear()

        # Draw our Scene
        self.scene.draw()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10, 10, arcade.csscolor.BLACK, 18)

        win_ = f"{self.win_text}"
        arcade.draw_text(win_, 0, SCREEN_HEIGHT/2, arcade.csscolor.BLACK, 100, SCREEN_WIDTH, align="center")

        final = f"{self.final_score}"
        arcade.draw_text(final, 0, SCREEN_HEIGHT/2-100, arcade.csscolor.BLACK, 60, SCREEN_WIDTH, align="center")

        to_reset = f"{self.reset_text}"
        arcade.draw_text(to_reset, 0, SCREEN_HEIGHT/2-170, arcade.csscolor.BLACK, 50, SCREEN_WIDTH, align="center")


    def process_keychange(self):
        # Process up
        if self.up_pressed:
            if (self.physics_engine.can_jump(y_distance=10) and not self.jump_needs_reset):
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                self.jump_needs_reset = True
                arcade.play_sound(self.jump_sound)

        # Process left/right
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0

        #Process reset
        if self.reset_pressed:
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0


    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.R:
            self.reset_pressed = True
            self.jump_needs_reset = False
            self.right_pressed = False
            self.left_pressed = False
            self.score = 1000
            self.setup()

        self.process_keychange()

    def on_key_release(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
        elif key == arcade.key.R:
            self.reset_pressed = False

        self.process_keychange()


    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()

        # Update animations
        if self.physics_engine.can_jump():
            self.player_sprite.can_jump = False
        else:
            self.player_sprite.can_jump = True


        # Update Animations
        self.scene.update_animation(
            delta_time,
            [
                LAYER_NAME_SPIKE,
                LAYER_NAME_DUCK,
                LAYER_NAME_BACKGROUND,
                LAYER_NAME_PLAYER,
            ],
        )



        player_collision_list = arcade.check_for_collision_with_lists(
            self.player_sprite,
            [
                self.scene[LAYER_NAME_SPIKE],
                self.scene[LAYER_NAME_DUCK],
            ],
        )


        for collision in player_collision_list:
            if self.scene[LAYER_NAME_DUCK] in collision.sprite_lists:
                arcade.play_sound(self.win)
                self.win_text = "You Win!"
                self.final_score = "Final Score: " + str(self.score)
                self.reset_text = "Press \"r\" to reset"
                collision.remove_from_sprite_lists()
                return
            self.scene[LAYER_NAME_SPIKE] in collision.sprite_lists
            arcade.play_sound(self.game_over)
            self.score -= 50
            collision.remove_from_sprite_lists()
            self.restart()
                
def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()