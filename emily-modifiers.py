import re
# define your ender here
unique_starters = ["STKPWHR"] # Mapped to ltrig(l,l)
LONGEST_KEY = 1

# RHS fingerspellings.
# I wanted ltrig hard press + motion to be used for vowels or misc. consonants otherwise not present on RHS like h and w.
# If there's ever overlaps/conflicts in steno characters, I just made a special combo or controller motion which adds a Z and/or * to differentiate.
fingerspells = {
  "-PLZ"      :"a", # M looks like A (ltrig(h) + RHS M = PLZ)
  "-B"        :"b",
  "-RBG"      :"c",
  "-D"        :"d",
  "-LT"       :"e", # T/F looks like E
  "-F"        :"f",
  "-G"        :"g",
  "-LS"       :"h", # H is kinda a vowel, right? lol
  "-PBLGZ"    :"i", # J looks like I (ltrig(h) + RHS J = PBLGZ)
  "-PBLG"     :"j",
  "-BG"       :"k",
  "-L"        :"l",
  "-PL"       :"m",
  "-PB"       :"n",
  "-LD"       :"o", # D looks like O
  "-P"        :"p",
  "*-PBLGZ"   :"q", # rstick(l,l,ul,u), like KW on LHS
  "-R"        :"r",
  "-S"        :"s",
  "-T"        :"t",
  "-BLG"      :"u", # K doesn't look like U, but U is for "up" and K is rstick(u)
  "*F"        :"v",
  "*-PLZ"     :"w", # rstick(l,l)
  "-BGS"      :"x",
  "-RPBLG"    :"y", # y = KWR on LHS, so y = RMK (R)(PL)(BG) on RHS
  "-Z"        :"z",
}

# F + direction = number, except # by itself is just 0, and L is 5.
numberspells = {
  "#":   "0",
  "#F":  "1",
  "FBG": "2",
  "FP":  "3",
  "FPL": "4",
  "FL":  "5",
  "FT":  "6",
  "FD":  "7",
  "FS":  "8",
  "FG":  "9",
}
# Function keys: F + R
fn_keyspells = {
  "#FR":   "F1",
  "FRBG":  "F2",
  "FRP":   "F3",
  "FRPL":  "F4",
  "FRL":   "F5",
  "FRT":   "F6",
  "FRD":   "F7",
  "FRS":   "F8",
  "FRG":   "F9",
  "#*R":   "F10",
  "#*FR":  "F11",
  "*FRBG": "F12",
}

def lookup(chord):
    if len(chord) != 1: raise KeyError
    assert len(chord) <= LONGEST_KEY

    match1 = re.fullmatch(r'(#?)([STKPWHR]*)([AO]*)([*-]*)([EU]*)([FRPBLGTSDZ]*)', chord[0])
    if match1 is None: raise KeyError
    (num, lhs, vowel1, seperator, vowel2, rhs) = match1.groups()
    modifiers = vowel1 + vowel2

    # If user doesn't specify the special starter or a modifier, then this dictionary has no use.
    if lhs not in unique_starters: raise KeyError
    if modifiers is None: raise KeyError

    # RHS stuff (and #) is what will determine fingerspelling.
    rhs = num + rhs

    if   rhs == "": output = "" # This is valid because you can may want to press the Windows key by itself.
    elif rhs in fingerspells: output = fingerspells[rhs]
    elif rhs in numberspells: output = numberspells[rhs]
    elif rhs in fn_keyspells: output = fn_keyspells[rhs]
    else: raise KeyError

    # Accumulate list of modifiers to be added to the output
    mods = []
    if "O" in modifiers: mods.append("shift")
    if "A" in modifiers: mods.append("control")
    if "U" in modifiers: mods.append("alt")
    if "E" in modifiers: mods.append("super")

    # Apply those modifiers
    for mod in mods: output = mod + "(" + output + ")"

    # Package it up with the syntax
    ret = "{#" + combo + "}"

    # Yay :D
    return ret
