import math


def A_g(params: dict) -> float:
    '''Gross area'''
    A_g = params.d*params.b
    return A_g


def I_x(params: dict) -> float:
    '''Moment of inertia - major axis'''
    I_x =params.b*params.d**3/12
    return I_x
    # return math.pi/64 * (params.d**4 - (params.d-2*params.t)**4)


def I_y(params: dict) -> float:
    '''Moment of inertia - minor axis'''
    I_y =params.d*params.b**3/12
    return I_y

# def S_x(params: dict) -> float:
#     '''Plastic section modulus - major axis'''
#     S_x = 2 * (A_g(params) / 2 * (params.d / 4))
#     return S_x


# def S_y(params: dict) -> float:
#     '''Plastic section modulus - minor axis'''
#     S_y =2 * (A_g(params) / 2 * (params.b / 4)) 
#     return S_y

def I_w(params: dict) -> float:
    '''Warping constant - NOT IMPLEMENTED'''
    I_w = 0
    return I_w  


def J(params: dict) -> float:
    '''Torsion constant - NOT IMPLEMENTED'''
    #J = 0
    a = max(params.d, params.b) #long side
    b = min(params.d, params.b) #short side
    J = a * b**3 * (1/3 - 0.21 * b / a * (1 - b**4 / (12*a**4)))
    return J


def main():
    ...
    
if __name__ == "__main__":
    main()
