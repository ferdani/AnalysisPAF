frfile = open("./singlefr.txt")

total_fakes = 0
for i, line in enumerate(frfile.readlines()):
  print line, i
  f = float(line)
  total_fakes += f/(1.-f)

print total_fakes
