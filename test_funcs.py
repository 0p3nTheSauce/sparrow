def test_point_funcs():
  from polygon import get_line_points, get_fill_boundaries, remove_duplicate_points
  og_points = [(3,0), (2,1),(3,1),(1,2),(2,2),(0,3),(1,3),(3,0),(3,1),(4,1),(4,2),(5,2),(5,3),(6,3)]
  print(f"OG points: {og_points}")
  sorted_by_y = sorted(og_points, key=lambda x: x[1])
  print(f"sorted by Y: {sorted_by_y}")
  singpnts_sortedBY = remove_duplicate_points(sorted_by_y)
  print(f"no duplicate points sorted by Y{singpnts_sortedBY}")
  
def main():
  test_point_funcs()

if __name__ == '__main__':
  main()