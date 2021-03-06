import random

class Vehicle:
    def __init__(self, wheelRadius, mass, friction, dt, 
                 initialX = 0, initialY = 0, 
                 initialVx = 0, initialVy = 0, 
                 initialOmegaX = 0, initialOmegaY = 0):
        self.x = initialX
        self.y = initialY
        self.vx = initialVx
        self.vy = initialVy
        self.omegaX = initialOmegaX
        self.omegaY = initialOmegaY
        self.wheelRadius = wheelRadius
        self.mass = mass
        self.friction = friction
        self.dt = dt
        
        self.encoderX = 0
        self.encoderY = 0
        self.ieee = [0, 0]
        
    def setMotor(self, omegaX, omegaY):
        self.omegaX = omegaX
        self.omegaY = omegaY
        
    def updateModel(self):
        newVx = self.wheelRadius * self.omegaX
        newVy = self.wheelRadius * self.omegaY
        
        # there is only 1 traction force since x and y are assumed to have 
        # the same friction coeff.
        tractionForce = self.friction * self.mass * 9.80665 
        acceleration = tractionForce / self.mass
        dv = acceleration * self.dt
        
        # if the absolute difference between desired and actual velocity 
        # is greater than dv, increment velocity by dv
        if (abs(newVx - self.vx) > dv): 
            if newVx > self.vx:
                self.vx = self.vx + dv
            else:
                self.vx = self.vx - dv
        # else (if the difference in desired vs actual is small) 
        # just set the velocity directly
        else:                           
            self.vx = newVx
            
        if (abs(newVy - self.vy) > dv):
            if newVy > self.vy:
                self.vy = self.vy + dv
            else:
                self.vy = self.vy - dv
        else:
            self.vy = newVy
        
        self.x += (self.vx  + random.gauss(0.01, 0.005)) * self.dt
        self.y += (self.vy  + random.gauss(0.01, 0.005)) * self.dt
        
        self.encoderX += self.omegaX * self.dt
        self.encoderY += self.omegaY * self.dt
        
        self.ieee[0] = self.x + random.gauss(0, 0.1)
        self.ieee[1] = self.y + random.gauss(0, 0.1)
        
    # encoder counts every 0.5 degrees, so convert from rad to deg, 
    # then multiply by 2    
    def readEncoder(self):              
        countsX = 2 * self.encoderX * 180 / 3.14159265359
        countsY = 2 * self.encoderY * 180 / 3.14159265359
        
        return (countsX, countsY)
        
    def readIEEE(self):
        return (self.ieee[0], self.ieee[1])
        
    def readActual(self):
        return (self.x, self.y)