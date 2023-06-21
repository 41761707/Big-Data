    pointers = []
    A = []
    A_sample_ids = []
    for window in range(0, round(len(data_stream) / window_length)):
        window_start = window * window_length
        stream = data_stream[window_start : window_start + window_length]
        # C_sample = data_stream[window * window_length : samples_in_window]
        C_sample_ids = []
        C = []
        for i, element in enumerate(stream):
            C.append(element)
            if i < samples_in_window:
                C_sample_ids.append(i)
            else:
                j = random.randint(0, i)
                if j < samples_in_window:
                    C_sample_ids[j] = i

            B = A[i + 1 :] + C
            print(f"A:{A}")
            print(f"B:{B}")
            print(f"C:{C}")
            print(f"C_samples:{C_sample_ids}")
            sliding_samples = ([A[a] for a in A_sample_ids if a > i]+[C[c] for c in C_sample_ids])[:samples_in_window]
            print(f"Sliding window:{sliding_samples}")
            pointers += sliding_samples
        A = C
        A_sample_ids = C_sample_ids
    return pointers

N = 100
stream = [i for i in range(N)]
window_length = 20
samples_in_window = 5
pointers = sliding_window(stream, window_length, samples_in_window)


plt.hist(pointers, density=True, bins=N)
plt.savefig(f"sliding_window_{window_length}_S{samples_in_window}.png")