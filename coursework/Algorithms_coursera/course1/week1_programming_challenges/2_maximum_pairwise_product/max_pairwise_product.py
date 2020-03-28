# python3


def max_pairwise_product(numbers):
	max1 = max(numbers)
	numbers.remove(max1)
	max2 = max(numbers)

	return max1 * max2


if __name__ == '__main__':
    input_n = int(input())
    input_numbers = [int(x) for x in input().split()]
    print(max_pairwise_product(input_numbers))
