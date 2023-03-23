import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms

def confidence_ellipse(x, y, ax, n_std=3.0, facecolor='none', **kwargs):
    """
    Create a plot of the covariance confidence ellipse of *x* and *y*.

    Parameters
    ----------
    x, y : array-like, shape (n, )
        Input data.

    ax : matplotlib.axes.Axes
        The axes object to draw the ellipse into.

    n_std : float
        The number of standard deviations to determine the ellipse's radiuses.

    **kwargs
        Forwarded to `~matplotlib.patches.Ellipse`

    Returns
    -------
    matplotlib.patches.Ellipse
    """
    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimensional dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,
                      facecolor=facecolor, **kwargs)

    # Calculating the standard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    # calculating the standard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)

# Team	            Rank        Final 16    Final 8,    Final 4     Total Min	Dim Min	    Avg Total Min	Avg Dim Min
germany 	    =   [1658.96,	False,      False,      False,	    417692,	    151562,	    16065,	        5829]
mexico          =   [1649.57,	False,	    False,      False,      380302,     150381,	    14627,	        5784]
england	        =   [1737.46,	True,	    True,       False,      344435,	    127588,	    13248,          4907]
switzerland	    =   [1621.43,	True,	    False,      False,      366774,	    120417,	    14107,	        4631]
brazil	        =   [1837.56,	True,	    True,       False,      328847,	    117771,	    12648,	        4530]
spain	        =   [1716.93,	True,	    False,      False,      239441,	    117359,	    9209,	        4514]
argentina       =   [1770.65,	True,	    True,       True,       236684,	    111168,	    9103,	        4276]
portugal        =   [1678.65,	True,	    True,       False,      321200,	    109550,	    12354,	        4213]
belgium	        =   [1821.92,	False,	    False,      False,      386820,	    105448,	    14878,	        4056]
qatar	        =   [1441.97,	False,	    False,      False,      303128,	    103468,	    11659,	        3980]
wales	        =   [1582.13,	False,	    False,      False,      257212,	    101313,	    9893,	        3897]
france	        =   [1764.85,	True,	    True,       True,       267270,	    96422,	    10691,	        3857]
netherlands     =   [1679.41,	True,	    True,       False,      237140,	    100107,	    9121,	        3850]
denmark	        =   [1665.47,	False,	    False,      False,      254925,	    97754,	    9805,	        3760]
canada	        =   [1473.82,	False,	    False,      False,      168529,	    89832,	    6482,	        3455]
croatia	        =   [1632.15,	True,	    True,       True,       208285,	    87053,	    8011,	        3348]
japan	        =   [1554.69,	True,	    False,      False,      202689,	    86093,	    7796,	        3311]
serbia	        =   [1549.53,	False,	    False,      False,      180288,	    80216,	    6934,	        3085]
uruguay	        =   [1640.95,	False,	    False,      False,      246111,	    78940,	    9466,	        3036]
tunisia	        =   [1507.86,	False,	    False,      False,      172560,	    78871,	    6637,	        3034]
ecuador	        =   [1463.74,	False,	    False,      False,      139936,	    76400,	    5382,	        2938]
southkorea	    =   [1526.02,	True,	    False,      False,      175776,	    74249,	    6761,	        2856]
saudiarabia     =   [1435.74,	False,	    False,      False,      131538,	    63615,	    5059,	        2447]
unitedstates    =   [1635.01,	True,	    False,      False,      128677,	    60562,	    4949,	        2329]
costarica	    =   [1500.06,	False,	    False,      False,      168104,	    60350,	    6466,	        2321]
senegal	        =   [1584.59,	True,	    False,      False,      110696,	    56312,	    4258,	        2166]
poland	        =   [1546.18,	True,	    False,      False,      164626,	    52209,	    6332,	        2008]
australia       =   [1483.73,	True,	    False,      False,      118407,	    51464,	    4554,	        1979]
iran	        =   [1558.64,	False,	    False,      False,      171680,	    47835,	    6867,	        1913]
morocco	        =   [1558.35,	True,	    True,       True,       92393,	    45044,	    3554,	        1732]
cameroon        =   [1484.95,	False,	    False,      False,      57048,	    29440,	    2194,	        1132]
ghana	        =   [1393.47,	False,	    False,      False,      52391,	    25418,	    2015,	        978]


teams = [germany, mexico, england, switzerland, brazil, spain, argentina, portugal, belgium, qatar, wales, france, netherlands, denmark, canada, croatia, japan, serbia, uruguay, tunisia, ecuador, southkorea, saudiarabia, unitedstates, costarica, senegal, poland, australia, iran, morocco, cameroon, ghana]



# ROUND OF 16: AVG DIM
plt.figure(1)
max_rank = teams[0][0]
min_rank = teams[0][0]
max_chem = teams[0][7]
min_chem = teams[0][7]

x_successful = []
y_successful = []
x_unsuccessful = []
y_unsuccessful = []

for team in teams:
    color = 'b' if team[1] else 'r'
    plt.scatter(team[0], team[7], c=color)

    if team[1]: 
        x_successful.append(team[0])
        y_successful.append(team[7])
    else:
        x_unsuccessful.append(team[0])
        y_unsuccessful.append(team[7])

    max_rank = team[0] if team[0] > max_rank else max_rank
    min_rank = team[0] if team[0] < min_rank else min_rank
    max_chem = team[7] if team[7] > max_chem else max_chem
    min_chem = team[7] if team[7] < min_chem else min_chem

y = ((max_chem - min_chem) / 2) + min_chem
x = ((max_rank - min_rank) / 2) + min_rank

plt.plot([min_rank, max_rank], [y, y], color='k')
plt.plot([x, x], [min_chem, max_chem], color='k')

confidence_ellipse(np.array(x_successful), np.array(y_successful),  plt.gca(), n_std=1, edgecolor='blue')
confidence_ellipse(np.array(x_unsuccessful), np.array(y_unsuccessful), plt.gca(), n_std=1, edgecolor='red')


# ROUND OF 8: AVG DIM
plt.figure(2)
max_rank = teams[0][0]
min_rank = teams[0][0]
max_chem = teams[0][7]
min_chem = teams[0][7]

x_successful = []
y_successful = []
x_unsuccessful = []
y_unsuccessful = []

for team in teams:
    color = 'b' if team[2] else 'r'
    plt.scatter(team[0], team[7], c=color)

    if team[2]: 
        x_successful.append(team[0])
        y_successful.append(team[7])
    else:
        x_unsuccessful.append(team[0])
        y_unsuccessful.append(team[7])

    max_rank = team[0] if team[0] > max_rank else max_rank
    min_rank = team[0] if team[0] < min_rank else min_rank
    max_chem = team[7] if team[7] > max_chem else max_chem
    min_chem = team[7] if team[7] < min_chem else min_chem

y = ((max_chem - min_chem) / 2) + min_chem
x = ((max_rank - min_rank) / 2) + min_rank

plt.plot([min_rank, max_rank], [y, y], color='k')
plt.plot([x, x], [min_chem, max_chem], color='k')

confidence_ellipse(np.array(x_successful), np.array(y_successful),  plt.gca(), n_std=1, edgecolor='blue')
confidence_ellipse(np.array(x_unsuccessful), np.array(y_unsuccessful), plt.gca(), n_std=1, edgecolor='red')

# ROUND OF 4: AVG DIM
plt.figure(3)
max_rank = teams[0][0]
min_rank = teams[0][0]
max_chem = teams[0][7]
min_chem = teams[0][7]

x_successful = []
y_successful = []
x_unsuccessful = []
y_unsuccessful = []

for team in teams:
    color = 'b' if team[3] else 'r'
    plt.scatter(team[0], team[7], c=color)

    if team[3]: 
        x_successful.append(team[0])
        y_successful.append(team[7])
    else:
        x_unsuccessful.append(team[0])
        y_unsuccessful.append(team[7])

    max_rank = team[0] if team[0] > max_rank else max_rank
    min_rank = team[0] if team[0] < min_rank else min_rank
    max_chem = team[7] if team[7] > max_chem else max_chem
    min_chem = team[7] if team[7] < min_chem else min_chem

y = ((max_chem - min_chem) / 2) + min_chem
x = ((max_rank - min_rank) / 2) + min_rank

plt.plot([min_rank, max_rank], [y, y], color='k')
plt.plot([x, x], [min_chem, max_chem], color='k')

confidence_ellipse(np.array(x_successful), np.array(y_successful),  plt.gca(), n_std=1, edgecolor='blue')
confidence_ellipse(np.array(x_unsuccessful), np.array(y_unsuccessful), plt.gca(), n_std=1, edgecolor='red')














# ROUND OF 4: AVG DIM
plt.figure(4)
max_rank = teams[0][0]
min_rank = teams[0][0]
max_chem = teams[0][7]
min_chem = teams[0][7]

x_successful = []
y_successful = []
x_unsuccessful = []
y_unsuccessful = []

for team in teams:
    color = 'b' if team[2] else 'r'
    if team[1]:
        plt.scatter(team[0], team[7], c=color)

        if team[2]: 
            x_successful.append(team[0])
            y_successful.append(team[7])
        else:
            x_unsuccessful.append(team[0])
            y_unsuccessful.append(team[7])
        
        max_rank = team[0] if team[0] > max_rank else max_rank
        min_rank = team[0] if team[0] < min_rank else min_rank
        max_chem = team[7] if team[7] > max_chem else max_chem
        min_chem = team[7] if team[7] < min_chem else min_chem

y = ((max_chem - min_chem) / 2) + min_chem
x = ((max_rank - min_rank) / 2) + min_rank

plt.plot([min_rank, max_rank], [y, y], color='k')
plt.plot([x, x], [min_chem, max_chem], color='k')

confidence_ellipse(np.array(x_successful), np.array(y_successful),  plt.gca(), n_std=1, edgecolor='blue')
confidence_ellipse(np.array(x_unsuccessful), np.array(y_unsuccessful), plt.gca(), n_std=1, edgecolor='red')















# ROUND OF 4: AVG DIM
plt.figure(5)
max_rank = teams[0][0]
min_rank = teams[0][0]
max_chem = teams[0][7]
min_chem = teams[0][7]

x_successful = []
y_successful = []
x_unsuccessful = []
y_unsuccessful = []

for team in teams:
    color = 'b' if team[3] else 'r'
    if team[2]:
        plt.scatter(team[0], team[7], c=color)

        if team[3]: 
            x_successful.append(team[0])
            y_successful.append(team[7])
        else:
            x_unsuccessful.append(team[0])
            y_unsuccessful.append(team[7])
        
        max_rank = team[0] if team[0] > max_rank else max_rank
        min_rank = team[0] if team[0] < min_rank else min_rank
        max_chem = team[7] if team[7] > max_chem else max_chem
        min_chem = team[7] if team[7] < min_chem else min_chem

y = ((max_chem - min_chem) / 2) + min_chem
x = ((max_rank - min_rank) / 2) + min_rank

plt.plot([min_rank, max_rank], [y, y], color='k')
plt.plot([x, x], [min_chem, max_chem], color='k')

confidence_ellipse(np.array(x_successful), np.array(y_successful),  plt.gca(), n_std=1, edgecolor='blue')
confidence_ellipse(np.array(x_unsuccessful), np.array(y_unsuccessful), plt.gca(), n_std=1, edgecolor='red')

plt.show()










