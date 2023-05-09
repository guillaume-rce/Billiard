# =================================================================
# =============          path: final\main.py          =============
# =============   author: Guillaume ROCHE [Fealinx]   =============
# =============            date: 2022/2023            =============
# =============             version: 1.0              =============
# =============    description: A billiard solveur    =============
# =================================================================

# %%

from modules.elements import BallStore, HoleStore, Table
from modules.last_trajectory import SelectTrajectories, TrajectoryStore

Rxs, Rys = [30, 40, 150, 20], [40, 30, 70, 60]
Yxs, Yys = [10, 40, 150], [80, 40, 10]
Wx, Wy = [100], [60]
Bx, By = [80], [90]

def main(
        red_xs, red_ys,
        yellow_xs, yellow_ys,
        white_x, white_y,
        black_x, black_y
    ) -> None:
    # Create a new BallStore and add some balls to it
    ball_store = BallStore()
    ball_store.add_balls(red_xs, red_ys, "red")
    ball_store.add_balls(yellow_xs, yellow_ys, "yellow")
    ball_store.add_balls(black_x, black_y, "black")
    ball_store.add_balls(white_x, white_y, "white")
    ball_store.set_players("red", "yellow")

    hole_store = HoleStore()  # Create a new HoleStore

    trajectory_store = TrajectoryStore()
    trajectory_store.add_trajectories(ball_store, hole_store)

    # Create a new Table
    table = Table()
    table.draw_table()  # Draw the table
    table.draw_holes(hole_store)  # Draw the holes

    # Display the balls on the table
    table.draw_balls(ball_store)

    trajectories = SelectTrajectories()
    trajectories.select_trajectories(trajectory_store, ball_store)

    table.draw_line(
        ball_store.get_white_ball(),
        trajectories.get_easiest().get_ball(),
        'white',
    )
    table.draw_line_by_coords(
        trajectories.get_easiest().get_ball().x,
        trajectories.get_easiest().get_ball().y,
        trajectories.get_easiest().get_hole().x,
        trajectories.get_easiest().get_hole().y,
        'white',
    )

    table.draw_line(
        ball_store.get_white_ball(),
        trajectories.get_hardest().get_ball(),
        'black',
    )
    table.draw_line_by_coords(
        trajectories.get_hardest().get_ball().x,
        trajectories.get_hardest().get_ball().y,
        trajectories.get_hardest().get_hole().x,
        trajectories.get_hardest().get_hole().y,
        'black',
    )

    table.display()
    # ------------------------------------------------------------
    # ------------------------------------------------------------

    print("Updating positions...")
    Rxs, Rys = [20, 30, 80, 50], [30, 30, 20, 60]
    Yxs, Yys = [10, 40, 150], [80, 40, 10]
    ball_store.update_positions(Rxs, Rys, "red")
    ball_store.update_positions(Yxs, Yys, "yellow")
    ball_store.set_players("red", "yellow")

    table.update_all(hole_store, ball_store)  # Update the table

    trajectory_store.update_trajectories(ball_store, hole_store)
    trajectories.update_trajectories(trajectory_store, ball_store)

    table.draw_line(
        ball_store.get_white_ball(),
        trajectories.get_easiest().get_ball(),
        'white',
    )
    table.draw_line_by_coords(
        trajectories.get_easiest().get_ball().x,
        trajectories.get_easiest().get_ball().y,
        trajectories.get_easiest().get_hole().x,
        trajectories.get_easiest().get_hole().y,
        'white',
    )

    table.draw_line(
        ball_store.get_white_ball(),
        trajectories.get_hardest().get_ball(),
        'black',
    )
    table.draw_line_by_coords(
        trajectories.get_hardest().get_ball().x,
        trajectories.get_hardest().get_ball().y,
        trajectories.get_hardest().get_hole().x,
        trajectories.get_hardest().get_hole().y,
        'black',
    )

    table.display()

if __name__ == "__main__":
    main(Rxs, Rys, Yxs, Yys, Wx, Wy, Bx, By)
# %%
