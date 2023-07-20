#这段触发器是在更改application的s前触发的，主要保证：
#1.所选原因序号未启用时s置2表示审核不通过。
#2.提交的用户以及违约无法再提交违约申请s置2表示审核不通过
#3.没有违约的用户的重生申请置2
#4.申请为违约申请时gather_all对应的年份，地区，行业违约申请数+1
#5.申请为重生申请时gather_all对应的年份，地区，行业重生申请数+1
#6.关联违约：所有该集团子公司全部关联违约。
#7.关联违约重生：解除所有该客户的集团子公司的关联违约。
#8.如果申请通过,客户的s置1表示违约
create trigger tr_on_application before update on application for each row
begin
    set @reason_id=0;
    select NEW.reason_id into @reason_id;
    set @reason_on=1;
    select on1 into @reason_on from reason where reason.reason_id=@reason_id;
    select s into @s from customer where new.cus_id=customer.cus_id;
    if(@reason_on=0) then
        set new.s=2;#'该原因未启用无法审核通过'
    elseif((@s=1 and NEW.c_or_w=1)or(new.c_or_w=0 and @s=0)) then
        set new.s=2;#'已违约的用户无法再次通过违约申请'没有违约的用户无法通过重生申请
    elseif(NEW.c_or_w=1 and new.s=1) then #申请为违约申请
        select com_id into @com_id from customer where customer.cus_id=NEW.cus_id;
        select industry,substr(location,1,3) into @industry,@area from company where com_id=@com_id; #拿到行业和地区（截取字符串前三位为某某区）
        select year(new.check_t) into @year;
        set @count1=0;set @count2=0;
        select ifnull(w_count,0) into @count1 from gather_all where industry=@industry and @year=year and area=@area;
        select ifnull(c_count,0) into @count2 from gather_all where industry=@industry and @year=year and area=@area;
        if(@count2=0 and @count1=0)then
            insert into gather_all values (@industry,@year,@area,1,0);
        else
            update gather_all set c_count=@count2,w_count=@count1+1 where industry=@industry and @year=year and area=@area;
        end if;
        if(new.reason_id=4) then#关联违约
            select com_id into @com_id from customer where customer.cus_id=NEW.cus_id;
            select g_game into @g_name from company where @com_id=com_id;
            update company set b=1 where g_game=@g_name; #所有该集团的公司全部关联违约
        else
            update customer set s=1 where cus_id=new.cus_id;
        end if;
    elseif(NEW.c_or_w=0 and new.s=1) then #申请为重生申请
        set @temp=100;#随便设一下
        select reason_id into @temp from application where app_id=(select max(app_id) from application where s=1 and cus_id=new.cus_id);
        if(@temp=new.reason_id) then
            select com_id into @com_id from customer where customer.cus_id=NEW.cus_id;
            select industry,substr(location,1,3) into @industry,@area from company where com_id=@com_id;
            select year(new.check_t) into @year;
            set @count1=0;set @count2=0;
            select ifnull(w_count,0) into @count1 from gather_all where industry=@industry and @year=year and area=@area;
            select ifnull(c_count,0) into @count2 from gather_all where industry=@industry and @year=year and area=@area;
            if(@count2=0 and @count1=0)then
                insert into gather_all values (@industry,@year,@area,0,1);
            else
                update gather_all set c_count=@count2+1,w_count=@count1 where industry=@industry and @year=year and area=@area;
            end if;
            if(new.reason_id=4) then #关联违约重生
                select com_id into @com_id from customer where customer.cus_id=NEW.cus_id;
                select g_game into @g_name from company where @com_id=com_id;
                update company set b=0 where g_game=@g_name; #关联违约集团公司关联违约标志置0
            else
                update customer set s=0 where cus_id=new.cus_id;
            end if;
        else
            set new.s=2;
        end if;
    end if;
end;
#该触发器在update company表上的b更新后触发
#1.关联违约：所有该公司集团的员工违约标记置1
#2.关联违约重生：除了非关联违约的客户，所有该集团的客户违约标志置0
create trigger tr_on_company after update on company for each row
begin
    if(old.b=0 and new.b=1) then
        update customer set s=1 where com_id=new.com_id; #所有关联违约的集团的员工全部违约
    elseif(old.b=1 and new.b=0)then
        #除了非关联违约的客户，所有该集团的客户违约标志置0
        update customer set s=0 where cus_id not in
        (select cus_id from
        (select cus_id from application where app_id in (select max(app_id) from application
        where cus_id in (select cus_id from customer where new.com_id=customer.com_id)  and application.s=1
        group by cus_id) and c_or_w=1 and reason_id!=4  and application.s=1)as a) and com_id=new.com_id;
    end if;
end;