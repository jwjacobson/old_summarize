
name1 = 'Stevenson, Robert Louis'
name2 = 'Von Arnim, Elizbeth'
name3 = 'Fitzgerald, F. Scott (Francis Scott)'


def author_parse(author):
    """
    Take the author information which is stored in Last, First Middle format and convert it to First Middle Last.
    For now it only handles the first author, so second authors of multiauthor books are out of luck.
    Examples:
    'Shelley, Mary Wollstonecraft' -> 'Mary Wollstonecraft Shelley'
    'Fitzgerald, F. Scott (Francis Scott)' -> 'F. Scott Fitzgerald'
    'Von Arnim, Elizbeth' -> 'Elizbeth Von Arnim'
    """
    parens = {'(', ')'}  # Parentheticals are used for full names of authors usually referred to as a letter, e.g. F Scott Fitzgerald
    vanvon = {'van', 'von'} # Names with van and von require special handling (also other compound last names....)
    split_author = author.split()
    while split_author[-1][-1] in parens or split_author[-1][0] in parens: # Remove parentheticals
        split_author.pop()
    last_name = split_author.pop(0) # last_name is not always the full last name, e.g. if it starts with van or von
    if last_name[-1] == ',':        # true last names end in comma, which is removed
        split_author.append(last_name[:-1])
    else:
        split_author.append(last_name)
    if split_author[-1].lower() in vanvon:  # if there is a van or von we need to pop one more time and remove the comma
        split_author.append(split_author.pop(0)[:-1])
    new_author = ' '.join(split_author)
    return new_author