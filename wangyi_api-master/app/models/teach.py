from peewee import *
from app.models.BaseModel import BaseModel

#database = MySQLDatabase('teach', **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT', 'use_unicode': True, 'host': '127.0.0.1', 'port': 3306, 'user': 'root', 'password': '123456'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

# class BaseModel(Model):
#     class Meta:
#         database = database

class GeArea(BaseModel):
    latitude = CharField(null=True)
    longitude = CharField(null=True)
    name = CharField(null=True)
    pid = IntegerField(index=True, null=True)
    region = IntegerField(null=True)
    statusa = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    zm = CharField(null=True)

    class Meta:
        table_name = 'ge_area'

class WqComment(BaseModel):
    comment_id = AutoField()
    content = CharField(null=True)
    question_id = IntegerField()
    user_id = IntegerField()

    class Meta:
        table_name = 'wq_comment'

class WqCourse(BaseModel):
    courseid = AutoField()
    coursename = CharField()
    coursestate = CharField()

    class Meta:
        table_name = 'wq_course'

class WqErrorbook(BaseModel):
    bookid = AutoField()
    courseid = CharField()
    gradeid = CharField()
    if_exist = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    questionid = CharField()
    remarks = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    typeid = CharField(null=True)
    uanswer = CharField()
    userid = CharField()

    class Meta:
        table_name = 'wq_errorbook'

class WqExam(BaseModel):
    exam_difficulty = CharField(null=True)
    exam_id = AutoField()
    exam_name = CharField()
    exam_question_type = CharField(null=True)
    exam_skill = CharField(null=True)
    position_id = IntegerField(null=True)

    class Meta:
        table_name = 'wq_exam'

class WqExamQuestionChapterTbl(BaseModel):
    is_parent = CharField(null=True)
    name = CharField(null=True)
    parent_cid = IntegerField(null=True)

    class Meta:
        table_name = 'wq_exam_question_chapter_tbl'

class WqExamQuestionTypeTbl(BaseModel):
    delete_flag = CharField(constraints=[SQL("DEFAULT '0'")], null=True)
    qt_abbr = CharField(null=True)
    qt_name = CharField(null=True)
    sequence = IntegerField(null=True)

    class Meta:
        table_name = 'wq_exam_question_type_tbl'

class WqExamPaperConfigTbl(BaseModel):
    ep_id = IntegerField(null=True)
    ep_ques_chapter = ForeignKeyField(column_name='ep_ques_chapter_id', field='id', model=WqExamQuestionChapterTbl, null=True)
    ep_ques_number = IntegerField(null=True)
    ep_ques_type = ForeignKeyField(column_name='ep_ques_type_id', field='id', model=WqExamQuestionTypeTbl, null=True)
    id = BigAutoField()

    class Meta:
        table_name = 'wq_exam_paper_config_tbl'

class WqExamQuestionMasterTbl(BaseModel):
    delete_date = DateTimeField(null=True)
    id = BigAutoField()
    insert_date = DateTimeField(null=True)
    pic_path = CharField(null=True)
    ques_chapter_ids = CharField(null=True)
    ques_content = TextField(null=True)
    ques_difficulties = CharField(null=True)
    ques_type = ForeignKeyField(column_name='ques_type_id', field='id', model=WqExamQuestionTypeTbl, null=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'wq_exam_question_master_tbl'

class WqExamPaperFinalTbl(BaseModel):
    delete_date = DateTimeField(null=True)
    exam_paper_id = IntegerField(null=True)
    exam_ques = ForeignKeyField(column_name='exam_ques_id', field='id', model=WqExamQuestionMasterTbl, null=True)
    exam_ques_type_id = IntegerField(null=True)
    insert_date = DateTimeField(null=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'wq_exam_paper_final_tbl'

class WqExamPaperMasterTbl(BaseModel):
    delete_date = DateTimeField(null=True)
    insert_date = DateTimeField(null=True)
    is_build_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    title = CharField(null=True)
    update_date = DateTimeField(null=True)

    class Meta:
        table_name = 'wq_exam_paper_master_tbl'

class WqExamPaperTemplateTbl(BaseModel):
    position = CharField(null=True)
    template = TextField(null=True)

    class Meta:
        table_name = 'wq_exam_paper_template_tbl'

class WqGrade(BaseModel):
    courseid = CharField()
    gradeid = AutoField()
    gradename = CharField()

    class Meta:
        table_name = 'wq_grade'

class WqHistory(BaseModel):
    last_time = DateTimeField()
    question_id = IntegerField(index=True)
    user_id = IntegerField(index=True)

    class Meta:
        table_name = 'wq_history'

class WqKnowledgePoint(BaseModel):
    collect = IntegerField(constraints=[SQL("DEFAULT 0")])
    content = TextField(null=True)
    father_id = IntegerField(constraints=[SQL("DEFAULT 0")], index=True, null=True)
    skill_name = CharField()

    class Meta:
        table_name = 'wq_knowledge_point'

class WqPaper(BaseModel):
    allowtime = CharField()
    begintime = CharField(null=True)
    courseid = CharField()
    endtime = CharField(null=True)
    gradeid = CharField()
    paperid = CharField()
    papername = CharField()
    paperstate = CharField(null=True)
    questionid = CharField()
    score = CharField(null=True)
    userid = CharField(null=True)

    class Meta:
        table_name = 'wq_paper'

class WqPaperQuestionRel(BaseModel):
    paper_id = IntegerField(index=True, null=True)
    q_id = IntegerField(index=True, null=True)
    q_order = IntegerField(null=True)
    rate = FloatField(null=True)
    score = IntegerField(null=True)

    class Meta:
        table_name = 'wq_paper_question_rel'

class WqPosition(BaseModel):
    position_desc = CharField()
    position_id = AutoField()
    position_name = CharField()
    position_request = CharField()

    class Meta:
        table_name = 'wq_position'

class WqQuestion(BaseModel):
    answer = CharField(null=True)
    answerdetail = CharField(null=True)
    collect = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    courseid = CharField(null=True)
    difficulty = IntegerField(null=True)
    gradeid = CharField(null=True)
    kp_id = IntegerField(null=True)
    optiona = CharField(null=True)
    optionb = CharField(null=True)
    optionc = CharField(null=True)
    optiond = CharField(null=True)
    quesname = CharField(null=True)
    questionid = AutoField()
    remark = CharField(null=True)
    typeid = CharField(null=True)
    useranswer = CharField(null=True)

    class Meta:
        table_name = 'wq_question'

class WqResources(BaseModel):
    description = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    kind = IntegerField(null=True)
    name = CharField()
    number = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    price = FloatField(null=True)
    state = IntegerField(constraints=[SQL("DEFAULT 1")], null=True)

    class Meta:
        table_name = 'wq_resources'

class WqSearchPath(BaseModel):
    bn_id = AutoField()
    end_question_id = IntegerField(null=True)
    start_question_id = IntegerField(null=True)
    time = IntegerField(null=True)

    class Meta:
        table_name = 'wq_search_path'

class WqStopWord(BaseModel):
    value = CharField(null=True)

    class Meta:
        table_name = 'wq_stop_word'

class WqTotalCollect(BaseModel):
    total_collect = IntegerField()

    class Meta:
        table_name = 'wq_total_collect'

class WqType(BaseModel):
    remark = CharField(null=True)
    score = IntegerField()
    typeid = AutoField()
    typename = CharField()

    class Meta:
        table_name = 'wq_type'

class WqUsers(BaseModel):
    access_token = CharField(null=True)
    address = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    app_id = CharField(column_name='appId', null=True)
    auth_key = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    created_at = IntegerField()
    email = CharField(null=True, unique=True)
    gender = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    grade = IntegerField(null=True)
    identity = IntegerField(constraints=[SQL("DEFAULT 1")], null=True)
    lastlogin = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    nickname = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    password = CharField(null=True)
    password_reset_token = CharField(null=True, unique=True)
    phone = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    realname = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    remarks = CharField(null=True)
    status = IntegerField(constraints=[SQL("DEFAULT 9")])
    unionid = CharField(constraints=[SQL("DEFAULT ''")])
    updated_at = IntegerField()
    updatetime = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    username = CharField(null=True, unique=True)
    verification_token = CharField(constraints=[SQL("DEFAULT ''")], null=True)

    class Meta:
        table_name = 'wq_users'

