from ctypes import *


class RimeTraits(Structure):
    _fields_ = [
        ("data_size", c_int),
        ("shared_data_dir", c_char_p),
        ("user_data_dir", c_char_p),
        ("distribution_name", c_char_p),
        ("distribution_code_name", c_char_p),
        ("distribution_version", c_char_p),
        ("app_name", c_char_p),
        ("modules", POINTER(c_char_p)),
        ("min_log_level", c_int),
        ("log_dir", c_char_p),
        ("preset_data_dir", c_char_p),
        ("staging_dir", c_char_p),
    ]


class RimeComposition(Structure):
    _fields_ = [
        ("length", c_int),
        ("cursor_pos", c_int),
        ("sel_start", c_int),
        ("sel_end", c_int),
        ("preedit", c_char_p),
    ]


class RimeCandidate(Structure):
    _fields_ = [
        ("text", c_char_p),
        ("comment", c_char_p),
        ("reserved", c_char_p),
    ]


class RimeMenu(Structure):
    _fields_ = [
        ("page_size", c_int),
        ("page_no", c_int),
        ("is_last_page", c_int),
        ("highlighted_candidate_index", c_int),
        ("num_candidates", c_int),
        ("candidates", POINTER(RimeCandidate)),
        ("select_keys", c_char_p),
    ]


class RimeCommit(Structure):
    _fields_ = [
        ("data_size", c_int),
        ("text", c_char_p),
    ]


class RimeContext(Structure):
    _fields_ = [
        ("data_size", c_int),
        ("composition", RimeComposition),
        ("menu", RimeMenu),
        ("commit_text_preview", c_char_p),
        ("select_labels", POINTER(c_char_p)),
    ]


class RimeStatus(Structure):
    _fields_ = [
        ("schema_id", c_char_p),
        ("schema_name", c_char_p),
        ("data_size", c_int),
        ("is_disabled", c_int),
        ("is_composing", c_int),
        ("is_ascii_mode", c_int),
        ("is_full_shape", c_int),
        ("is_simplified", c_int),
        ("is_traditional", c_int),
        ("is_ascii_punct", c_int),
    ]


class RimeCandidateListIterator(Structure):
    _fields_ = [
        ("ptr", c_void_p),
        ("index", c_int),
        ("candidate", RimeCandidate),
    ]


class RimeConfig(Structure):
    _fields_ = [
        ("ptr", c_void_p),
    ]


class RimeConfigIterator(Structure):
    _fields_ = [
        ("list", c_void_p),
        ("map", c_void_p),
        ("index", c_int),
        ("key", c_char_p),
        ("path", c_char_p),
    ]


class RimeSchemaListItem(Structure):
    _fields_ = [
        ("schema_id", c_char_p),
        ("name", c_char_p),
        ("reserved", c_char_p),
    ]


class SchemaList(Structure):
    _fields_ = [
        ("size", c_size_t),
        ("list", POINTER(RimeSchemaListItem)),
    ]


def RIME_STRUCT_INIT(type, var):
    var.data_size = sizeof(type)
    return var


def get_candidate(input: str):
    rime = CDLL("./rime.dll")
    rime.RimeSetup(POINTER(c_int)())
    rime.RimeInitialize(POINTER(c_int)())
    rime.RimeCreateSession.restype = POINTER(c_uint)
    session_id = rime.RimeCreateSession()
    rime.RimeSimulateKeySequence(session_id, input.encode("utf-8"))
    commit = RimeCommit()
    RIME_STRUCT_INIT(RimeCommit, commit)
    context = RimeContext()
    RIME_STRUCT_INIT(RimeContext, context)

    result = ""
    rime.RimeFreeCommit(byref(commit))
    if rime.RimeGetCommit(session_id, byref(commit)):
        result += commit.text.decode("utf-8")
    rime.RimeFreeContext(byref(context))
    rime.RimeGetContext(session_id, byref(context))

    # 不知为何无法退出 for 循环，所以直接在 for 里 return
    for candidate in context.menu.candidates:
        try:
            return result + candidate.text.decode("utf-8")
        except:
            return result if result else "未能找到候选词"
