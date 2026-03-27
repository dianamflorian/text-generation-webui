import html as html_module

THINKING_FORMATS = [
    ('<think>', '</think>', None),
    ('<|channel|>analysis<|message|>', '<|end|>', '<|channel|>final<|message|>'),
    ('<|channel|>commentary<|message|>', '<|end|>', '<|channel|>final<|message|>'),
    ('<seed:think>', '</seed:think>', None),
    ('<|think|>', '<|end|>', '<|content|>'),              
                                                                                                                                             
    (None, '</think>', None),                                       
]

def extract_reasoning(text, html_escaped=False):
    """Extract reasoning/thinking blocks from the beginning of a string.

    When html_escaped=True, tags are HTML-escaped before searching
    (for use on already-escaped UI strings).

    Returns (reasoning_content, final_content) where reasoning_content is
    None if no thinking block is found.
    """
    if not text:
        return None, text

    esc = html_module.escape if html_escaped else lambda s: s

    for start_tag, end_tag, content_tag in THINKING_FORMATS:
        end_esc = esc(end_tag)
        content_esc = esc(content_tag) if content_tag else None

        if start_tag is None:
                                                                    
            end_pos = text.find(end_esc)
            if end_pos == -1:
                continue
            thought_start = 0
        else:
                                              
            start_esc = esc(start_tag)
            start_pos = text.find(start_esc)
            if start_pos == -1:
                                                                            
                stripped = text.strip()
                if stripped and start_esc.startswith(stripped):
                    return '', ''
                continue
            thought_start = start_pos + len(start_esc)
            end_pos = text.find(end_esc, thought_start)

        if end_pos == -1:
                                                                          
            if content_esc:
                content_pos = text.find(content_esc, thought_start)
                if content_pos != -1:
                    thought_end = content_pos
                    content_start = content_pos + len(content_esc)
                else:
                    thought_end = len(text)
                    content_start = len(text)
            else:
                thought_end = len(text)
                content_start = len(text)
        else:
            thought_end = end_pos
            if content_esc:
                content_pos = text.find(content_esc, end_pos)
                if content_pos != -1:
                    content_start = content_pos + len(content_esc)
                else:
                                                                          
                    content_start = end_pos + len(end_esc)
            else:
                content_start = end_pos + len(end_esc)

        return text[thought_start:thought_end], text[content_start:].lstrip()

    for marker in ['<|start|>assistant<|channel|>final<|message|>', '<|channel|>final<|message|>']:
        marker_esc = esc(marker)
        pos = text.find(marker_esc)
        if pos != -1:
            before = text[:pos].strip()
            after = text[pos + len(marker_esc):]
            return (before if before else None), after

    return None, text
