import numpy as np
# from scipy import signal
# from scipy import ndimage

import helpers.test_helpers_and_creators as test_helpers_and_creators

def downsizing_data(a_vec, b_vec):

# --------------------

    #TODO - these are former stuff regarding true lfp's:

    # a_median = signal.medfilt(a_vec, kernel_size=11)
    # b_median = signal.medfilt(b_vec, kernel_size=11)

    # win = signal.windows.hann(50)
    # a_filtered = signal.convolve(a_vec, win, mode='same') / sum(win)
    # b_filtered = signal.convolve(b_vec, win, mode='same') / sum(win)

    # # a_filtered = ndimage.uniform_filter1d(a_vec, size=11)
    # # b_filtered = ndimage.uniform_filter1d(b_vec, size=11)

    # # show the original graphs
    # test_helpers_and_creators.plot_graph(a_vec, " a_vec", (min(a_vec), max(a_vec)))
    # test_helpers_and_creators.plot_graph(b_vec, " b_vec", (min(b_vec), max(b_vec)))

    # # a_filtered = a_filtered[100:1000]
    # # b_filtered = b_filtered[100:1000]

    # a_filtered = a_filtered.astype(int)
    # b_filtered = b_filtered.astype(int)

    # # show the new filtered graphs
    # test_helpers_and_creators.plot_graph(a_filtered, " new a_filtered", (min(a_filtered), max(a_filtered)))
    # test_helpers_and_creators.plot_graph(b_filtered, " new b_filtered", (min(b_filtered), max(b_filtered)))

# --------------------

    # narrow down the amount of angles
    new_a_filtered = np.array([])
    new_b_filtered = np.array([])
   
    min_diff_thresh = 1

    # take the first coordinates of a_vec, b_vec
    # in each iter compare the curr item to the last element appended to new_a_filtered, new_b_filtered
    # if the difference is bigger then the threshold, append these coordinates as well  

    new_a_filtered = np.append(new_a_filtered, a_vec[0])
    new_b_filtered = np.append(new_b_filtered, b_vec[0])

    # append only couples that are different in at least min_diff_thresh units (in at least one angle)
    for i in range(1, len(a_vec)):
        if(abs(new_a_filtered[-1] - a_vec[i]) > min_diff_thresh  
            and abs(new_b_filtered[-1] -b_vec[i]) > min_diff_thresh):
            new_a_filtered = np.append(new_a_filtered,a_vec[i])
            new_b_filtered = np.append(new_b_filtered,b_vec[i])
            

    print(len(a_vec))
    print(new_a_filtered.shape[0])

    test_helpers_and_creators.plot_graph(new_a_filtered, " new new_a_filtered", (min(new_a_filtered), max(new_a_filtered)))
    test_helpers_and_creators.plot_graph(new_b_filtered, " new new_b_filtered", (min(new_b_filtered), max(new_b_filtered)))

    print()

    return new_a_filtered, new_b_filtered
