import re
# define your ender here
unique_starters = ["STKPWHR"] # Mapped to ltrig(l,l)
LONGEST_KEY = 1

# RHS fingerspellings.
# I wanted ltrig light press (-R) + motion to be used for vowels or misc. consonants otherwise not present on RHS like h and w.
# If there's ever overlaps/conflicts in steno characters, I just made a special combo or controller motion which adds a Z and/or * to differentiate.
fingerspells = {
  "RPL"      :"a", # M looks like A
  "B"        :"b",
  "RBG"      :"c",
  "D"        :"d",
  "RT"       :"e", # T/F looks like E
  "F"        :"f",
  "G"        :"g",
  "RS"       :"h", # H is kinda a vowel, right? lol
  "RPBLGZ"   :"i", # J looks like I (ltrig(l) + RHS Y = PBLGZ)
  "PBLG"     :"j",
  "BG"       :"k",
  "L"        :"l",
  "PL"       :"m",
  "PB"       :"n",
  "RD"       :"o", # D looks like O
  "P"        :"p",
  "PBGSDZ"   :"q", # rstick(l,l,ul,u), like KW on LHS
  "R"        :"r",
  "S"        :"s",
  "T"        :"t",
  "RG"       :"u", # G doesn't look like U, but U is for "up" and K is rstick(u)
  "*F"       :"v",
  "PSDZ"     :"w", # rstick(l,l), like W on LHS
  "GS"       :"x",
  "BGS"      :"x",
  "RPBLG"    :"y", # y = KWR on LHS, so y = RMK (R)(PL)(BG) on RHS
  "Z"        :"z",
}

# L + direction = number, except # by itself is just 0, and L is 5.
numberspells = {
  "#":    "0",
  "#L":   "1",
  "*LG":  "2",
  "PLZ":  "3",
  "PLSZ": "4",
  "*L":   "5",
  "LT":   "6",
  "LG":   "7",
  "LS":   "8",
  "LD":   "9",
}
# Function keys: R + L
fn_keyspells = {
  "#RL":   "F1",
  "RBLG":  "F2",
  "RPL":   "F3",
  #"RPL":  "F4", # Already taken by "a"
  "*RL":   "F5",
  "RLT":   "F6",
  "RLG":   "F7",
  "RLS":   "F8",
  "RLD":   "F9",
  "#*R":   "F10",
  "#*RL":  "F11",
  "*RBLG": "F12",
}

def lookup(chord):
    if len(chord) != 1: raise KeyError
    assert len(chord) <= LONGEST_KEY

    print('chord',chord)
    match1 = re.fullmatch(r'(#?)([STKPWHR]*)([AO]*)[-]?([*]?)([EU]*)([FRPBLGTSDZ]*)', chord[0])
    if match1 is None: raise KeyError
    (num, lhs, vowel1, asterisk, vowel2, rhs) = match1.groups()
    modifiers = vowel1 + vowel2
    print('lhs',lhs)
    print('mod',modifiers)

    # If user doesn't specify the special starter or a modifier, then this dictionary has no use.
    if lhs not in unique_starters: raise KeyError
    if modifiers is None: raise KeyError

    # RHS stuff (and #) is what will determine fingerspelling.
    rhs = num + asterisk + rhs
    print('rhs',rhs)

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

    # Package it up with the syntax. But only if we need to, b/c {#} makes things non-undoable which is annoying when just fingerspelling letters or numbers.
    if len(mods)>0 or rhs in fn_keyspells:
        output = "{#" + output + "}"
        print('yes')
        print(len(mods))
    print('ret',output)

    # Yay :D
    return output
