E_ELEC = 50e-9
EPS_SHORT = 10e-9
EPS_LONG = 0.0013e-9
PACKET_SIZE = 500  # Bytes (data)
OVERHEAD_SIZE =125 # Bytes
E_agg = 50e-9
d_0 = (EPS_SHORT/EPS_LONG)**0.5
k = (PACKET_SIZE + OVERHEAD_SIZE) * 8  # Total #of Tx bits


class Node():
    def __init__(self,x=0,y=0):
        self._energy = 2
        self._dead = False
        self._x = x
        self._y = y
        self._MODE = "node"

    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, x1):
        self._x = x1

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, y1):
        self._y = y1
    
    @property
    def energy(self):
        return self._energy
    
    @energy.setter
    def energy(self, e):
        self._energy = e 

    @property
    def MODE(self):
        return self._MODE
    
    @MODE.setter
    def MODE(self, m):
        self._MODE = m


    def get_position(self):
        return self._x, self._y
        
  
     
    # Calculate d from this node to the sink
    def calculate_distance(self, x_s, y_s):
        d = ((x_s - self.get_position()[0])**2 
            + (y_s - self.get_position()[1])**2) **0.5
        
        return d
    
    
    def calculate_energy(self,x_s,y_s):
        dist = self.calculate_distance(x_s,y_s)
        if dist <= d_0: # Short Distance
            return (k * E_ELEC) + (k * EPS_SHORT * (dist**2))

        return (k * E_ELEC) + (k * EPS_LONG  * (dist**4))
    

    def _consume_node(self, x_s, y_s):
        if not self._dead:
            E_tx = self.calculate_energy(x_s,y_s)
            if self._energy - E_tx < 0:
                self._dead = True
                # print('I cannot communicate!')
            else:
                self._energy = self._energy - E_tx
    
    def _consume_head(self, x_s, y_s):
        E_rx = k*E_ELEC
        E_tx = self.calculate_energy(x_s, y_s)
        E_agg_total = k * E_agg
        
        E_total = E_rx + E_tx + E_agg_total

        if self._energy - E_total < 0:
                self._dead = True
        else:
            self._energy = self._energy - E_total
        
        
    
    def consume_energy(self, x_s, y_s):
        if self._MODE == "node":
            self._consume_node(x_s, y_s)
        else:
            self._consume_head(x_s, y_s)
        
        
        
    def isDead(self):
        return self._dead
        
    # Calculate distance to another node
    def distance_to_node(self, other):
        d = ((other.get_position()[0] - self.get_position()[0])**2 
            + (other.get_position()[1] - self.get_position()[1])**2) **0.5
        
        return d
    
    # Check if it needs dualihop..
    def dual_hop(self, x_s, y_s, R):
        dist = self.calculate_distance(x_s,y_s)
        if dist > R:
            return True
        return False
    
    def set_dead(self):
        self._dead = True


