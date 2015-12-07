def gini(list_of_values):
  sorted_list = sorted(list_of_values)
  height, area = 0, 0
  for value in sorted_list:
    height += value
    area += height - value / 2.
  fair_area = height * len(list_of_values) / 2
  return (fair_area - area) / fair_area
	
if __name__ == '__main__':
	print gini([1,2.2,3.2,4,3,3,3,555,6672,123])