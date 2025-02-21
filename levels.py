FACTOR = 1 # the nearest to 0 the faster the cooldown
LEVEL_DATA = {
    #       m       p(d)       p(t)      p(e)      n      kinds (k)
    0:      (1,     0.00,       0,        0,        0,      1),  
    1:      (1,     0.10,       0,        0,        0,      1),
    2:      (1,     0.15,       0,        0,        0,      2),
    3:      (1,     0.2,        0.05,     0.02,     1,      2),
    5:      (2,     0.25,       0.05,     0.05,     1,      2),
    7:      (2,     0.3,        0.05,     0.05,     1,      2),
    10:     (1,     0.35,       0.05,     0.05,     1,      3),
    13:     (1,     0.4,        0.1,      0.06,     1,      3),
    16:     (2,     0.45,       0.1,      0.07,     1,      3),
    20:     (2,     0.5,        0.1,      0.08,     2,      3),
    24:     (1,     0.55,       0.2,      0.1,      2,      4),
    28:     (1,     0.6,        0.2,      0.1,      2,      4),
    33:     (1,     0.65,       0.2,      0.11,     3,      4),
    38:     (2,     0.7,        0.2,      0.12,     3,      4),
    43:     (2,     0.75,       0.2,      0.12,     3,      4),
    49:     (2,     0.8,        0.3,      0.14,     3,      4),
    55:     (3,     0.83,       0.3,      0.15,     4,      4),
    61:     (3,     0.86,       0.4,      0.16,     4,      4),
    67:     (3,     0.9,        0.4,      0.17,     4,      4),
    73:     (4,     0.91,       0.4,      0.18,     4,      4),
    79:     (4,     0.92,       0.4,      0.2,      4,      4),
    85:     (4,     0.93,       0.45,     0.2,      4,      4),
    91:     (4,     0.94,       0.45,     0.2,      5,      4),
    97:     (5,     0.95,       0.50,     0.2,      5,      4),
    }


"""
    Updates the player's attributes and the asteroid field based on the current level.
    Parameters:
    player (Player): The player object whose attributes will be updated.
    level (int): The current level of the game.
    asteroids_field (AsteroidField): The asteroid field object whose attributes will be updated.
    The LEVEL_DATA dictionary contains tuples with the following elements:
 
    - m (multiplicity) (int): The number of asteroids spawned per second. 
        m = asteroids_field.multiplicity 
    - p(d) (float): The probability of the player having double shot power.
        p(d) = player.power["double"]
    - p(t) (float): The probability of the player having triple shot power. p(t) <= p(d)
        p(t) = player.power["triple"]
    - p(e) (float): The probability of an explosion occurring.
        p(e) = player.power["explosion"]["prob"]
    - n (int): The number of shots in every explosion.
        n = player.power["explosion"]["num"]

    THE FORMULA

    power of fire = factor * m * 26 / 4
    Factor is a number near 1 (0.8, 0.7...)
    11 / 3 is the average increment of the asteroid field size when a new asteroid is spawned
        - Size 10 need 10 shots to be destroyed
    
    power of fire = (1 + p(d) + p(t) + n*p(e)) * frecuency of shoots
    frecuency of shoots = 1 / shoot_cooldown

    So
    shoot_cooldown = (1 + p(d) + p(t) + n*p(e)) * (3 / (11 * m * factor))
    """
def calculate_shoot_cooldown(level):
    """
    Calculate the shoot cooldown based on the current level.
    Parameters:
    level (int): The current level of the game.
    Returns:
    float: The shoot cooldown.
    """
    if level in LEVEL_DATA:
        m, p_d, p_t, p_e, n, k = LEVEL_DATA[level]
        print("    m  , p(d) , p(t) , p(e) ,  n  ,  k  ")
        print(f"{m: 5}, {p_d: 5}, {p_t: 5}, {p_e: 5}, {n: 5}, {k: 5}")
        power_of_one_shoot = (1 + p_d + p_t) # A shoot can be single, double or triple. 
        power_of_explosion = n * p_e
        power_of_destruction = power_of_one_shoot + power_of_explosion

        average_field_increment = 1
        if k == 2: 
            average_field_increment = 2
        elif k == 3:
            average_field_increment = 11 / 3
        elif k == 4: 
            average_field_increment = 26 / 4

        asteroids_field_increment_per_second = m * average_field_increment
        print("Power of one shoot: ", power_of_one_shoot)
        print("Power of explosion: ", power_of_explosion)
        print("Power of destruction: ", power_of_destruction)
        print("Asteroids field increase rate per spawn: ", average_field_increment)
        print("Asteroids field increase rate per second: ", asteroids_field_increment_per_second)
        result = FACTOR * power_of_destruction / asteroids_field_increment_per_second
        print("new cooldown: ", result)
        return result

    return calculate_shoot_cooldown(level - 1)