from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from django.template import loader
from .models import *
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.models import auth, User
from django.contrib.auth import logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import cx_Oracle


class Error(Exception):
    """Base class for other exceptions"""
    pass


def welcome(request):
    return render(request, "ipl2021/welcome.html")


def login(request):
    try:
        if request.method == 'POST':
            if request.POST.get('username') and request.POST.get('password') :
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = auth.authenticate(username=username, password = password)
                if user is not None:
                    auth.login(request, user)
                    return HttpResponseRedirect("/")
                else:
                    messages.error(request, 'Invalid Credentials')
                    return render(request, "ipl2021/login.html")
        else:
            return render(request, "ipl2021/login.html")
    except ValueError as ve:
        messages.error(request, 'Enter Username')
        return render(request, 'ipl2021/login.html')


def thanks(request):
    return render(request, "ipl2021/thanks.html")


def signup(request):
    try:
        if request.method == 'POST':
            if request.POST.get('username') and request.POST.get('password') :
                if request.POST.get('repassword') == request.POST.get('password') :
                    username = request.POST.get('username')
                    password = request.POST.get('password')
                    user = User.objects.create_user(username = username , password=password)
                    user.save()
                    messages.success(request, 'User Created successfully')
                else :
                    raise Error("Password Mismatch")
            return render(request, 'ipl2021/relogin.html')
        else:
            return render(request, 'ipl2021/signup.html')
    except IntegrityError as e:
        messages.error(request, 'Username exists')
        return render(request, 'ipl2021/signup.html')
    except Error as e :
        messages.error(request, 'Password Mismatch')
        return render(request, 'ipl2021/signup.html')


def relogin(request):
    return render(request, "ipl2021/relogin.html")


def home(request):
    if request.user.is_authenticated:
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='oracle')

        db = cx_Oracle.connect(user=r'devtest', password='Oracle123')
        cursor = db.cursor()
        sql='''with f as (select player_id , points from (select sum(points) points,player_id from final_Table group by player_id order by 1 desc)where rownum =1)
               select p.name , f.points from players p , f  where f.player_id = p.player_id'''

        cursor.execute(sql)
        mat_det = cursor.fetchall()
        content = {"points" : mat_det}
        cursor.execute('''select name , win||'/'||total from (select p.name , count(*) win ,( select count(*) from matches where who_win is not null) total 
                            from final_table f, players p where win_loss ='Y' and p.player_id = f.player_id group by p.name order by 2 desc) where rownum=1''')
        mat_det = cursor.fetchall()
        content['wins'] = mat_det
        cursor.execute('''with m as  (select max(match_id) max_match from matches where who_win is not null)
                          select p.name , points from (
                            select player_id , sum(points) points from  final_table f, m where f.match_id between m.max_match - 6 
                               and m.max_match group by player_id order by 2 desc)fs,
                            players p where p.player_id = fs.player_id and rownum =1''')
        mat_det = cursor.fetchall()
        content['week'] = mat_det
        cursor.execute('''select name , runs from (
                            select name , sum(runs_scored) runs from match_details md, selection s, players p 
                            where s.match_id = md.match_id and s.player_id  = p.player_id and s.team = md.team 
                            group by name order by 2 desc) where rownum=1
                            union all
                            select name , fours from (
                            select name , sum(fours_hit) fours from match_details md, selection s, players p 
                            where s.match_id = md.match_id and s.player_id  = p.player_id and s.team = md.team 
                            group by name order by 2 desc) where rownum=1
                            union all
                            select name , sixes from (
                            select name , sum(sixes_hit) sixes from match_details md, selection s, players p 
                            where s.match_id = md.match_id and s.player_id  = p.player_id and s.team = md.team 
                            group by name order by 2 desc) where rownum=1
                            union all
                            select name , wickets from (
                            select name , sum(wickets) wickets from match_details md, selection s, players p 
                            where s.match_id = md.match_id and s.player_id  = p.player_id and s.team = md.team 
                            group by name order by 2 ) where rownum=1''')
        mat_det = cursor.fetchall()
        content['runs'] = mat_det
        print(content)
        return render(request, "ipl2021/home.html", content)
    else:
        return HttpResponseRedirect("login/")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def matches(request):
    if request.user.is_authenticated:
        query_results = Matches.objects.all()
        p = Paginator(query_results, 10)
        page_num = request.GET.get('page', 1)
        try :
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
        content = {'query': page}
        return render(request, "ipl2021/matches.html", content)
    else:
        return HttpResponseRedirect("login/")


def matchdetails(request, who_win):

    if request.user.is_authenticated:
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='oracle')

        db = cx_Oracle.connect(user=r'devtest', password='Oracle123')
        cursor = db.cursor()
        sql='''select md.team, m.match_id , runs_scored, fours_hit, sixes_hit, wickets, won ,  'vs '||replace(replace(match, team),'-')
                            from matches m, match_details md where md.match_id = m.match_id and team = :who_win'''
        cursor.execute(sql,who_win= who_win)
        mat_det = cursor.fetchall()
        p = Paginator(mat_det, 7)
        page_num = request.GET.get('page', 1)
        try :
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
        content = {'query': page}
        return render(request, "ipl2021/matchdetails.html", content)
    else:
        return HttpResponseRedirect("login/")


def players(request):

    if request.user.is_authenticated:
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='oracle')

        db = cx_Oracle.connect(user=r'devtest', password='Oracle123')
        cursor = db.cursor()
        cursor.execute('''with s as (select player_id, sum(decode(power_game,'Y',1,0)) power_games, sum(decode(team, 'N/A', 0, 1)) 
                                            no_played from selection s group by player_id) 
                            select rank() over (order by points desc) "Rank" , name "Name",  no_wins "Wins", 
                                   points "Points" , s.power_games "PG_Used"
                            from (select  p.player_id ,p.name,sum(decode(win_loss,'Y',1,0)) No_Wins, sum(points) Points , max(points) highest_point
                                     from final_table f, players p where p.player_id = f.player_id 
                                    group by p.player_id , p.name order by 4 desc) p , s
                            where p.player_id = s.player_id''')
        det_list = cursor.fetchall()
        p = Paginator(det_list, 7)
        page_num = request.GET.get('page', 1)
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
        details = {'details': page}
        return render(request, "ipl2021/players.html", details)
    else:
        return HttpResponseRedirect("login/")


def playerdetails(request, name):

    if request.user.is_authenticated:
        dsn_tns = cx_Oracle.makedsn('localhost', '1521', service_name='oracle')

        db = cx_Oracle.connect(user=r'devtest', password='Oracle123')
        cursor = db.cursor()
        sql = ''' select p.name, m.match, s.team, decode(s.team , m.who_win, 'Y', 'N') "W/L", s.power_game 
                    from players p , selection s , matches m 
                   where p.player_id = s.player_id
                     and m.match_id = s.match_id
                     and p.name =:name
                     order by m.match_id'''
        cursor.execute(sql, name=name)
        det_list = cursor.fetchall()
        p = Paginator(det_list, 7)
        page_num = request.GET.get('page', 1)
        try:
            page = p.page(page_num)
        except EmptyPage:
            page = p.page(1)
        details = {'details': page}
        return render(request, "ipl2021/playerdetails.html", details)
    else:
        return HttpResponseRedirect("login/")