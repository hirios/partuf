import pymem


indexPattern = bytes.fromhex("80 37 8F 3C") #Apparently this is the hex corresponding to the number 1016018816
mem = pymem.memory


def process_scan(handle: int, pattern: bytes, end_address: int = 0x7FFFFFFFFFFF):
  next_region = 0
  lista = []

  while next_region < end_address:
    try:
        next_region, found = pymem.pattern.scan_pattern_page(handle, next_region, pattern, return_multiple=True)
        if found:
          for x in found:
            lista.append(x)

    except:
        next_region += 2437591040

  return lista


pm = pymem.Pymem('HD-Player.exe')
handle = pm.process_handle
lista = process_scan(handle, indexPattern)

for x in lista:
    mem.write_int(handle, x, 16018816)