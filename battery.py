from random import randint

class battery:
    # UL U UR
    # L X R
    # DL D DR
    def __init__(self, coord_battery, shape_env, gaussian_env):
        self.coord_battery = coord_battery
        self.shape_env = shape_env
        self.direction = self.__get_random_direction()
        self.gaussian_env = gaussian_env
        # low prev condition = bad, high prev condition = good
        self.prev_condition = gaussian_env[coord_battery[0]][coord_battery[1]]
        self.movements = [self.coord_battery]
        self.food = 0
    
    
    def movement(self):
        if self.__is_possible_direction(self.direction):
            # keep on that direction
            print("KEEP ON!")
            self.coord_battery = self.__step_in_direction(self.direction)
        else:
            # take a step in a random direction
            print("CHANGE DIRECTION!")
            new_direction = self.direction
            while new_direction == self.direction:
                new_direction = self.__get_random_direction()
            self.direction = new_direction
            self.coord_battery = self.__step_in_direction(self.direction)
        
        self.movements.append(self.coord_battery)
        self.prev_condition = self.gaussian_env[self.coord_battery[0]][self.coord_battery[1]]
    
    
    def __is_possible_direction(self, direction):        
        pds = self.__get_possible_directions()
        if direction not in pds:
            return False
        
        proj_coord = self.__step_in_direction(direction)
        # if the condition improves continue
        if self.prev_condition < self.gaussian_env[proj_coord[0]][proj_coord[1]]:
            return True
        else:
            return False
        
    
    def __get_possible_directions(self):
        # possible coordinates
        d = self.__get_dict_directions()
        
        possible_directions = []
        for key in d.keys():
            x_m, y_m = d[key]
            
            if x_m >= 0 and x_m < self.shape_env[0] and y_m >= 0 and y_m < self.shape_env[1]:
                possible_directions.append(key)
        
        return possible_directions
    
    
    def __get_random_direction(self):
        pds = self.__get_possible_directions()
        return pds[randint(0, len(pds)-1)]
    
    
    def __step_in_direction(self, direction):       
        return self.__get_dict_directions()[direction]
    
    
    def __get_dict_directions(self):
        d = dict()
        x, y = self.coord_battery
        d["UL"] = (x-1, y-1)
        d["U"] = (x-1, y)
        d["UR"] = (x-1, y+1)
        d["L"] = (x, y-1)
        d["R"] = (x, y+1)
        d["DL"] = (x+1, y-1)
        d["D"] = (x+1, y)
        d["DR"] = (x+1, y+1)
        
        return d