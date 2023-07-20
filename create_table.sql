create table customer(
  cus_id char(5) primary key,#主键客户ID
  name varchar(50),#客户姓名
  s integer,#违约状态（1/0表示是否违约）这是为了实现一个客户只能违约一次的标记，如果s=1那就不能再通过客户的违约申请。
  com_id char(5)#对应的公司ID
);
create table application(
    app_id char(5) primary key,#申请单号主码
    c_or_w integer,#0/1表示其为重生申请还是违约申请。
    check_t date,#审核人审核完成的时间
    file blob,#传附件
    s integer,#0/1表示是否审核完成，0：待审核，1：审核完成并且通过，2：审核完成并且不通过
    severe varchar(4),#违约严重程度（高，中，低）
    app_time date,#申请人发起该申请的时间
    app_acc char(5),#申请人账号（谁发起申请的）
    check_acc char(5),#审核人账号（谁审核完成的）
    reason_id integer,#违约原因序号
    cus_id char(5)#客户ID
);
create table app_p(
    name varchar(50),#申请人名字
    app_acc char(5) primary key,#申请人账号
    password varchar(12)#申请人密码
);
create table check_p(
    name varchar(50),#审核人名字
    check_acc char(5) primary key,#审核人账号
    password varchar(12)#审核人密码
);
create table reason(#这个表是违约原因表不包括重生原因！
    reason_id integer primary key,#原因序号
    on1 integer,#原因是否开启
    rea_detail varchar(500)#原因详细说明
);
create table company(
    com_id char(5) primary key,#公司ID
    name varchar(50),#公司名称
    b integer,#是否关联违约标记0/1
    location varchar(200),#公司地址格式为（某某区什么什么号）统一一下便于操作
    g_game varchar(50),#集团名称
    industry varchar(50)#行业
);
create table gather_all(
    industry varchar(50),#行业
    year char(4),#年份
    area varchar(20),#地区
    w_count integer,#违约个数
    c_count integer,#重生个数
    primary key (industry,year,area)
);