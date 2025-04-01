def test_point_funcs():
  from polygon import get_line_points, get_fill_boundaries, remove_duplicate_points
  og_points = [(3,0), (2,1),(3,1),(1,2),(2,2),(0,3),(1,3),(3,0),(3,1),(4,1),(4,2),(5,2),(5,3),(6,3)]
  print(f"OG points: {og_points}")
  sorted_by_y = sorted(og_points, key=lambda x: x[1])
  print(f"sorted by Y: {sorted_by_y}")
  singpnts_sortedBY = remove_duplicate_points(sorted_by_y)
  remaining_points = singpnts_sortedBY
  print(f"no duplicate points sorted by Y{singpnts_sortedBY}")
  y_min,y_max = singpnts_sortedBY[0][1],singpnts_sortedBY[-1][1]
  for i in range(y_min,y_max+1):
    line_pnts, remaining_points = get_line_points(remaining_points, i)
    print(f"Line points for line {i}: {line_pnts}")
    fill_bounds = get_fill_boundaries(line_pnts)
    print(f"Fill boundaries for line {i}: {fill_bounds}")

def test_process_points():
  from polygon import seperate_lines, get_fill_boundaries, remove_duplicate_points
  og_points = [(3,0), (2,1),(3,1),(1,2),(2,2),(0,3),(1,3),(3,0),(3,1),(4,1),(4,2),(5,2),(5,3),(6,3)]
  rem_dup = remove_duplicate_points(og_points)
  sorted_by_y = sorted(rem_dup, key=lambda x: x[1])
  print(f'og points: {og_points}')
  print(f'no duplicates {rem_dup}')
  print(f'sorted {sorted_by_y}')
  
  proc_points = seperate_lines(sorted_by_y)
  for i, line in enumerate(proc_points):
    print(f'Line points for line {i}: {line}')
    fill_bounds = get_fill_boundaries(line)
    print(f"Fill boundaries for line {i}: {fill_bounds}")

def test_find_edges():
  from polygon import find_in_edges, in_2_edges
  og_points = [(3,0), (2,1),(3,1),(1,2),(2,2),(0,3),(1,3),(3,0),(3,1),(4,1),(4,2),(5,2),(5,3),(6,3)]
  edges = [[(3,0), (2,1),(3,1),(1,2),(2,2),(0,3),(1,3)], [(3,0),(3,1),(4,1),(4,2),(5,2),(5,3),(6,3)]]
  point = (3,0)
  found1 = find_in_edges(point, edges)

  print(f'Point {point} found in edges: ')
  print(found1)
  print()
  nbrs1_on2 = [(3,0)]
  nbrs2_on2 = [(2,1),(3,1),(4,1)]
  nbrs3_off2 = [(1,2), (2,2)]
  nbrs4_off2 = [(4,2), (5,2)]
  nbrs5_off2 = [(0,3),(1,3)]
  nbrs6_off2 = [(5,3),(6,3)]
  print(f"Neighbours {nbrs1_on2} on 2 edges: {in_2_edges(nbrs1_on2, edges)} ")
  print(f"Neighbours {nbrs2_on2} on 2 edges: {in_2_edges(nbrs2_on2, edges)}")
  print(f"Neighbours {nbrs3_off2} on 2 edges: {in_2_edges(nbrs3_off2, edges)}")
  print(f"Neighbours {nbrs4_off2} on 2 edges: {in_2_edges(nbrs4_off2, edges)}")
  print(f"Neighbours {nbrs5_off2} on 2 edges: {in_2_edges(nbrs5_off2, edges)}")
  print(f"Neighbours {nbrs6_off2} on 2 edges: {in_2_edges(nbrs6_off2, edges)}")
def main():
  #test_point_funcs()
  # test_process_points()
  test_find_edges()
if __name__ == '__main__':
  main()