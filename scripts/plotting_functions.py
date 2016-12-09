from path_definition import scripts_dir

def plot_tracked_ratings(list_of_fg_to_track, elo_tracking_dict, glicko_tracking_dict, skill_tracking_dict, name, key_location):
    """Function to plot the track of the TrueSkill, Glicko and Elo ratings for a list of functional_groups (MAX = 7]"""
    
    sns.set(color_codes=True)
    plt.rcParams['xtick.labelsize'] = 15
    plt.rcParams['ytick.labelsize'] = 15
    
    fig, (ax1, ax2, ax3) = plt.subplots(1,3,figsize=(15,15))
    fig.subplots_adjust(wspace = 0.3)
        
    colors = ["K", "r", "g", "c", "m", "y", "k"]

    num = 0
    #elos
    for fg in list_of_fg:
        elo_y_vals = [float(i) for i in elo_tracking_dict[fg]]
        elo_x_vals = [ind[0] for ind in enumerate(elo_y_vals)]
        ax1.set_xlim((-5,200))
        ax1.set_ylim((0,2000))
        ax1.scatter(elo_x_vals, elo_y_vals, c=colors[num], alpha = 1.0, label = fg, edgecolor = "none")
        x1,x2 = ax1.get_xlim()
        y1,y2 = ax1.get_ylim()
        ax1.set_aspect(abs(x2-x1)/abs(y2-y1))
        ax1.set_xlabel("Number of Competitions", fontsize=17)
        ax1.set_ylabel("Elo Rating", fontsize=17)
        num += 1
        handles, labels = ax1.get_legend_handles_labels()
        ax1.legend(handles, labels, loc = key_location)
        
    num = 0
    #glickos
    for fg in list_of_fg:
        gli_y_vals = [i.mu for i in glicko_tracking_dict[fg]]
        gli_x_vals = [ind[0] for ind in enumerate(gli_y_vals)]
        ax2.set_xlim((-5,200))
        ax2.set_ylim((0,2500))
        ax2.scatter(gli_x_vals, gli_y_vals, c=colors[num], alpha = 1.0, label = fg, edgecolor = "none")
        x3,x4 = ax2.get_xlim()
        y3,y4 = ax2.get_ylim()
        ax2.set_aspect(abs(x4-x3)/abs(y4-y3))
        ax2.set_xlabel("Number of Competitions", fontsize=17)
        ax2.set_ylabel("Glicko Rating", fontsize=17)
        num += 1
        handles, labels = ax1.get_legend_handles_labels()
        ax2.legend(handles, labels, loc = key_location)
        
    num = 0        
    for fg in list_of_fg:
        skill_y_vals = [list(i)[0] for i in skill_tracking_dict[fg]]
        skill_x_vals = [ind[0] for ind in enumerate(skill_y_vals)]
        ax3.set_xlim((-5,200))
        ax3.set_ylim((0,50))
        ax3.scatter(skill_x_vals, skill_y_vals, c=colors[num], alpha = 1.0, label = fg, edgecolor = "none")
        x5,x6 = ax3.get_xlim()
        y5,y6 = ax3.get_ylim()
        ax3.set_aspect(abs(x6-x5)/abs(y6-y5))
        ax3.set_xlabel("Number of Competitions", fontsize=17)
        ax3.set_ylabel("TrueSkill" + ur"$^{\u2122}$" + "Rating", fontsize=17)
        num += 1
        handles, labels = ax1.get_legend_handles_labels()
        ax3.legend(handles, labels, loc = key_location)
        
        os.chdir(scripts_dir)
        os.chdir("../pictures")
        plt.savefig(name + ".png", bbox_inches="tight")
