import time
from kesslergame import Scenario, KesslerGame, GraphicsType
from ControllerCodeFromDrDick import ScottDickController
from YbnController import YbnController
# from graphics_both import GraphicsBoth
import sys

# Define game scenario
my_test_scenario = Scenario(name='Test Scenario',
                            num_asteroids=10,
                            ship_states=[
                                {'position': (400, 400), 'angle': 90, 'lives': 3, 'team': 1, "mines_remaining": 3},
                                # {'position': (400, 600), 'angle': 90, 'lives': 3, 'team': 2, "mines_remaining": 3},
                            ],
                            map_size=(1000, 800),
                            time_limit=60,
                            ammo_limit_multiplier=0,
                            stop_if_no_ammo=False)

# Define Game Settings
game_settings = {'perf_tracker': True,
                 'graphics_type': GraphicsType.Tkinter,
                 'realtime_multiplier': 1,
                 'graphics_obj': None,
                 'frequency': 30}

game = KesslerGame(settings=game_settings)  # Use this to visualize the game scenario
# game = TrainerEnvironment(settings=game_settings)  # Use this for max-speed, no-graphics simulation

# Evaluate the game
pre = time.perf_counter()
controllers = []

controller_args = sys.argv[1:]
if len(controller_args) > 0:
    for c_arg in controller_args:
        if (c_arg.lower() == "ybn"):
            controllers.append(YbnController())
        elif (c_arg.lower() == "scott"):
            controllers.append(ScottDickController())
        else:
            print(f"Skipping unknown controller {c_arg}")
else:
    controllers = [ScottDickController()]

score, perf_data = game.run(scenario=my_test_scenario, controllers=controllers)

# Print out some general info about the result
print('Scenario eval time: '+str(time.perf_counter()-pre))
print(score.stop_reason)
print('Asteroids hit: ' + str([team.asteroids_hit for team in score.teams]))
print('Deaths: ' + str([team.deaths for team in score.teams]))
print('Accuracy: ' + str([team.accuracy for team in score.teams]))
print('Mean eval time: ' + str([team.mean_eval_time for team in score.teams]))