from settings import *


def multi(win):
    
    # Draw paddles
    paddle1 = Rectangle(Point(20, 250), Point(30, 350))  # Left paddle
    paddle1.setFill("white")
    paddle1.draw(win)

    paddle2 = Rectangle(Point(770, 250), Point(780, 350))  # Right paddle
    paddle2.setFill("white")
    paddle2.draw(win)

    # Draw ball
    ball_start_x = WINDOW_WIDTH / 2 + random.choice([-50, 50]) 
    ball_start_y = WINDOW_HEIGHT / 2
    ball = Circle(Point(ball_start_x, ball_start_y), 10)
    ball.setFill("white")
    ball.draw(win)

    # Draw shorter moving target, avoiding the ball's initial position
    target_start_y = random.randint(100, 400)  # Random vertical position away from ball's center
    target = Rectangle(Point(390, target_start_y), Point(410, target_start_y + 100))  # Center paddle
    target.setFill("red")
    target.draw(win)

    # Initialize scores
    score1 = 0
    score2 = 0
    score_display = Text(Point(WINDOW_WIDTH / 2, 50), f"{score1} - {score2}")
    score_display.setTextColor("white")
    score_display.setSize(20)
    score_display.draw(win)

    # Ball velocity
    dx = random.choice([-5, 5])  # Randomize initial direction
    dy = random.choice([-5, 5])


    # Target velocity
    target_dy = 3

    # Game loop
    while True:
        # Move the ball
        ball.move(dx, dy)
        ball_center = ball.getCenter()


        # Check for wall collisions (top and bottom)
        if ball_center.getY() <= 10 or ball_center.getY() >= 590:
            dy = -dy

        # Move the target back and forth
        target.move(0, target_dy)
        if target.getP1().getY() <= 10 or target.getP2().getY() >= WINDOW_HEIGHT - 10:
            target_dy = -target_dy

        # Check for paddle collisions
        if (20 <= ball_center.getX() - 5 <= 30 and 
            paddle1.getP1().getY() <= ball_center.getY() <= paddle1.getP2().getY()):
            dx = -dx
            ball.move(10, 0)  # Move ball slightly away to prevent sticking
        if (770 <= ball_center.getX() + 5 <= 780 and 
            paddle2.getP1().getY() <= ball_center.getY() <= paddle2.getP2().getY()):
            dx = -dx
            ball.move(-10, 0)  # Move ball slightly away to prevent sticking

        # Check for collisions with the target
        if (target.getP1().getX() <= ball_center.getX() <= target.getP2().getX() and
            target.getP1().getY() <= ball_center.getY() <= target.getP2().getY()):
            if dx < 0:  # Left player hits the target
                score2 += 1
            else:  # Right player hits the target
                score1 += 1
            score_display.setText(f"{score2} | {score1}")
            dx = -dx  # Reverse ball direction
            ball.move(20 if dx > 0 else -20, 0)  # Move ball away to prevent sticking

        # Check for point loss (side wall collision)
        if ball_center.getX() < 0:  # Left player loses a point
            score2 -= 1
            score_display.setText(f"{score2} | {score1}")
            ball.move(ball_start_x - ball_center.getX(), ball_start_y - ball_center.getY())
            dx, dy = random.choice([-5, 5]), random.choice([-5, 5])  # Reset ball velocity
        elif ball_center.getX() > 800:  # Right player loses a point
            score1 -= 1
            score_display.setText(f"{score2} | {score1}")
            ball.move(ball_start_x - ball_center.getX(), ball_start_y - ball_center.getY())
            dx, dy = random.choice([-5, 5]), random.choice([-5, 5])  # Reset ball velocity

        # Paddle movement (use key inputs)
        key = win.checkKey()
        if key == "w" and paddle1.getP1().getY() > 0:
            paddle1.move(0, -20)
        elif key == "s" and paddle1.getP2().getY() < 600:
            paddle1.move(0, 20)
        elif key == "Up" and paddle2.getP1().getY() > 0:
            paddle2.move(0, -20)
        elif key == "Down" and paddle2.getP2().getY() < 600:
            paddle2.move(0, 20)

        # End the game when a player reaches 10 points
        if score1 >= 5 or score2 >= 5:
            clear_window(win)
            time.sleep(1)
            winner = "Left Player Wins!" if score1 >= 5 else "Right Player Wins!"
            exit = message_menu(winner, win)
            return exit
            
            

        # End the game when the other player reaches -5 points
        if score1 <= -3 or score2 <= -3:
            clear_window(win)
            time.sleep(1)
            winner = "Right Player Wins!" if score2 >= -3 else "Left Player Wins!"
            exit = message_menu(winner, win)
            return exit
            

        time.sleep(0.02)  # Slow down the loop

        # Escape sequence
        if key == 'Escape':
            break