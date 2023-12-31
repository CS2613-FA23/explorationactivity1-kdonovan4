import arcade

# Constants for screen
SCREEN_WIDTH = 1248
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Jump It"

# Constants used to scale sprites
TILE_SCALING = 1
CHARACTER_SCALING = TILE_SCALING
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

# Movement speeds for player, movement and jump speed are in pixels per frame
PLAYER_MOVEMENT_SPEED = 10
GRAVITY = 1.4
PLAYER_JUMP_SPEED = 25

# Constants for player spawn point
PLAYER_START_X = 2
PLAYER_START_Y = 1

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

# Constants for layer names within MapFinal.JSON
LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_BACKGROUND = "Background"
LAYER_NAME_PLAYER = "Player"
LAYER_NAME_SPIKE = "Spike"
LAYER_NAME_DUCK = "Duck"

# Loads a pair of textures, one for right-facing and the other for left-facing
def load_texture_pair(filename):
    return [arcade.load_texture(filename), arcade.load_texture(filename, flipped_horizontally=True)]

class Entity(arcade.Sprite):
    def __init__(self, name_folder, name_file):
        super().__init__()

        # Default to facing right
        self.facing_direction = RIGHT_FACING

        # Load textures
        self.idle_texture_pair = load_texture_pair("assets/Base_Model.png")
        self.jump_texture_pair = load_texture_pair("assets/Jump.png")
        self.walk_textures = load_texture_pair("assets/Walk.png")

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Set hit box
        self.set_hit_box(self.texture.hit_box_points)


class PlayerCharacter(Entity):
    def __init__(self):

        # Set up parent class
        super().__init__("assets", "Base_Model.png")

        # Track if jumping
        self.jumping = False

    def update_animation(self, delta_time: float = 1 / 60):
        # Check if need to face right or left
        if self.change_x < 0 and self.facing_direction == RIGHT_FACING:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == LEFT_FACING:
            self.facing_direction = RIGHT_FACING

        # Jumping
        if self.change_y > 0 or self.change_y < 0:
            self.texture = self.jump_texture_pair[self.facing_direction]
            return

        # Idle
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.facing_direction]
            return

        # Walking
        self.texture = self.walk_textures[self.facing_direction]


class JumpIt(arcade.Window):
    def __init__(self):
        # Call the parent class to set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Initialize the current state of which keys are pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.jump_needs_reset = False
        self.reset_pressed = False

        # Initialize tile mao
        self.tile_map = None

         # Initialize scene
        self.scene = None

        # Initialize player sprite
        self.player_sprite = None

        # Initialize physics engine
        self.physics_engine = None

         # Initialize score
        self.score = 1000

        # Initialize end screen text
        self.win_text = ""
        self.final_score = ""
        self.reset_text = ""

        # Load sounds
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")
        self.win = arcade.load_sound(":resources:sounds/upgrade1.wav")


    def setup(self):
        # TileMap name
        map_name = "assets/MapFinal.JSON"

        # Layer Options for the Tilemap, using true for every object that doesn't move
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

        # Loading in TileMap and setting as scene
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options, None, "Simple", 4.5, (-48,0))
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Set up the player and placing it at spawn point
        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_x = (self.tile_map.tile_width * TILE_SCALING * PLAYER_START_X)
        self.player_sprite.center_y = (self.tile_map.tile_height * TILE_SCALING * PLAYER_START_Y)
        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)


        # Creating the physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            gravity_constant=GRAVITY,
            walls=self.scene[LAYER_NAME_PLATFORMS]
        )

        # Resetting the end screen text for if restart is used
        self.win_text = ""
        self.final_score = ""
        self.reset_text = ""

    def restart(self):
        # Reseting player locaton to spawn point, resetting x and y speed to 0, and turning off key presses so you don't keep moving on respawn until you release and press again
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0
        self.jump_needs_reset = False
        self.right_pressed = False
        self.left_pressed = False
        self.player_sprite.center_x = (self.tile_map.tile_width * TILE_SCALING * PLAYER_START_X)
        self.player_sprite.center_y = (self.tile_map.tile_height * TILE_SCALING * PLAYER_START_Y)

    def on_draw(self):
        # Clear the screen
        self.clear()

        # Draw the Scene
        self.scene.draw()

        # Drawing text elements onto the screen, the last three will be invisible until the end screen
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
        # Check if up
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True

        # Check if left
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True

        # Check if right
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        
        # Check if r
        elif key == arcade.key.R:
            self.reset_pressed = True
            self.jump_needs_reset = False
            self.right_pressed = False
            self.left_pressed = False
            self.score = 1000
            self.setup()

        # Once you know the new key, process it
        self.process_keychange()

    def on_key_release(self, key, modifiers):
        # Check if up
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
        
        # Check if left
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False

         # Check if right
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

        # Check if r
        elif key == arcade.key.R:
            self.reset_pressed = False
        
        # Once you know the missing key, process it
        self.process_keychange()


    def on_update(self, delta_time):
        # Move the player with the physics engine
        self.physics_engine.update()

        # Update animations and jump state
        if self.physics_engine.can_jump():
            self.player_sprite.can_jump = False
        else:
            self.player_sprite.can_jump = True

        # Update animations for each layer in the TileMap
        self.scene.update_animation(
            delta_time,
            [
                LAYER_NAME_SPIKE,
                LAYER_NAME_DUCK,
                LAYER_NAME_BACKGROUND,
                LAYER_NAME_PLAYER,
            ],
        )

        # Making a list of all collisions player is currently touching
        player_collision_list = arcade.check_for_collision_with_lists(
            self.player_sprite,
            [
                self.scene[LAYER_NAME_SPIKE],
                self.scene[LAYER_NAME_DUCK],
            ],
        )

        # Processing each collision, displaying end screen if duck, removing spike otherwise
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

# Start up function                
def main():
    window = JumpIt()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()