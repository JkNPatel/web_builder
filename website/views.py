from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import auth
from django.utils import timezone
from django.views import View
from .models import CustomUser
from .models import Website
from .models import Page
from .models import Counter
from .models import PageElement
from .models import Meta
from .models import SubUser
from .models import SubUserAccess
from .models import Header
from .models import Menu1
from .models import Menu2
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
import time
from datetime import datetime
from django.core.files.storage import FileSystemStorage


# Create your views here.

class UserLogin(View):
    def post(self,request):
        if 'next' in self.request.GET:
            nextPage = request.GET['next']
            print(nextPage)
        else:
            nextPage = 'website:dashboard'
        email = request.POST['email']
        password = request.POST['password']
        error_msg = ''

        try:
            validate_email(email)
            valid_email = True
        except ValidationError:
            valid_email = False

        if valid_email == True:
            user = auth.authenticate(email=email,password=password)
            if user is not None:
                auth.login(request, user)
                print('login successfull')
                print(user.last_login)
                return redirect(nextPage)
                
            else:
                error_msg = 'Email and Password does not match'
                return render(request,'porto/pages/login.html',{'error':error_msg})
        else:
            error_msg = 'Invalid Email'
            return render(request,'porto/pages/login.html',{'error':error_msg})
       

    def get(self,request):
        return render(request,'porto/pages/login.html')

class UserLogout(View):
    def get(self,request):
        logout(request)
        return redirect('website:login')

class UserRegister(View):
    def post(self,request):
        email = request.POST['email']
        password = request.POST['password']
        repeat_password = request.POST['repeat_password']
        error_msg = ''
        is_user_exist = CustomUser.objects.filter(email=email)

        try:
            validate_email(email)
            valid_email = True
        except ValidationError:
            valid_email = False

        if is_user_exist.count()>0:
            error_msg = 'Email is already registered'
            return render(request,'porto/pages/register.html',{'error':error_msg})
        else:
            if valid_email == True:
                if(password == repeat_password):
                    user = CustomUser.objects.create_user(email=email,is_active=True,password=password)
                    user.save()
                    return redirect('website:login')
                else:
                    error_msg = 'Password does not match'
                    return render(request,'porto/pages/register.html',{'error':error_msg})
            else:
                error_msg = 'Invalid Email'
                return render(request,'porto/pages/register.html',{'error':error_msg})

    def get(self,request):
        return render(request,'porto/pages/register.html')

class All_sub_user(View):
    def get(self,request):
        print('sub user')

        websites = Website.objects.filter(website_user_id=request.user.id)
        sub_users = SubUser.objects.filter(sub_user_owner_id=request.user.id)


        id = self.request.GET.get('id', None)

        if(id != "" and id != None):
            delete_users = SubUser.objects.filter(pk=id)
            
            if(delete_users.count()==1):
                delete_users[0].delete()
                return redirect('website:sub_users')
            else:
                return redirect('website:sub_users')

        return render(request,'porto/pages/all_user.html',{'websites':websites,'sub_users':sub_users})

    def post(self,request):

        if 'add_user' in request.POST:
            print('add_user')
            username = request.POST['username']
            password = request.POST['password']

            is_sub_user_exist = SubUser.objects.filter(sub_user_uname=username)

            if(is_sub_user_exist.count() == 0):
                new_user = SubUser.objects.create(sub_user_uname= username,sub_user_pass=password,sub_user_owner_id=request.user.id)
                new_user.save()
            else:
                print('already exits')

        if 'save_changes' in request.POST:
            print('edit changes')
            id = request.POST['sub_user_id']
            edit_password = request.POST['edit_password']
            is_sub_user_exist = SubUser.objects.filter(pk=id)

            print(is_sub_user_exist)

            if(is_sub_user_exist.count() == 1 ):
               
                for each in is_sub_user_exist:
                    each.sub_user_pass = edit_password
                    each.save()

        return redirect('website:sub_users')


class Sub_user_access(View):
    def get(self,request):
        print('sub user access')

        
        websites = Website.objects.filter(website_user_id=request.user.id)
        sub_users = SubUser.objects.filter(sub_user_owner_id=request.user.id)
        
        sub_users_access = SubUserAccess.objects.filter(sub_access_owner_id = request.user.id)

        id = self.request.GET.get('id', None)

        if(id != "" and id != None):
            delete_users = SubUserAccess.objects.filter(pk=id)
            
            if(delete_users.count()==1):
                delete_users[0].delete()
                return redirect('website:subuser_access')
            else:
                return redirect('website:subuser_access')

        return render(request,'porto/pages/website_access.html',{'websites':websites,'sub_users':sub_users,'sub_user_access':sub_users_access})

    def post(self,request):

        if 'add_user_access' in request.POST:
            print('grant changes')
            
            add_website = request.POST['add_website']
            add_sub_user = request.POST['add_sub_user']
            print(add_website)
            print(add_sub_user)
            
            is_sub_user_access_exist = SubUserAccess.objects.filter(sub_access_user_id_id = add_sub_user).filter(sub_access_website_id_id = add_website )

            if(is_sub_user_access_exist.count() == 0):
                new_user_access = SubUserAccess.objects.create(sub_access_user_id_id = add_sub_user ,sub_access_website_id_id = add_website ,sub_access_owner_id=request.user.id)
                new_user_access.save()
            else:
                print('already exits')
           

        return redirect('website:subuser_access')

class UserDashboard(LoginRequiredMixin,View):
    login_url = '/login'
    #redirect_field_name = 'index'
    def post(self,request):
        
        return redirect('website:dashboard')
    
    def get(self,request):
        
        id = self.request.GET.get('website_id', None)

        if(id != "" and id != None):
            delete_website = Website.objects.filter(pk=id)
            print(delete_website.count())
            if(delete_website.count()==1):
                print('in loop')
                for each in delete_website:
                    if(each.website_is_active == 1):
                        print('change')
                        each.website_is_active = 0
                        each.save()
                    else:
                        each.website_is_active = 1
                        each.save()

                return redirect('website:dashboard')
            else:
                return redirect('website:dashboard')

        websites = Website.objects.filter(website_user_id=request.user.id)


            
        print('----------')
        print(websites)
        return render(request,'porto/pages/dashboard.html',{'websites':websites})

class AddWebsite(View):
    def post(self,request):
        website_name = request.POST['name']
        website_url = request.POST['url']
        
        website_logo = request.FILES['1_image']
        fs = FileSystemStorage(location='media/logo/')
        name = fs.save(time.strftime("%Y%m%d_%H%M%S")+".png",website_logo)
        logo_url = fs.url(name)
        
        favicon_logo = request.FILES['2_image']
        fs = FileSystemStorage(location='media/logo/')
        name1 = fs.save(time.strftime("%Y%m%d_%H%M%S")+".png",favicon_logo)
        favicon_url = fs.url(name1)

        website = Website.objects.create(website_user_id=request.user, website_name=website_name,website_url=website_url, website_logo1 = logo_url[1:] , website_favicon = favicon_url[1:])
        website.save()
        return redirect('website:dashboard')

    def get(self,request):
        return render(request,'porto/pages/website_information.html')

class MasterEdit(View):
    def post(self,request):
        table = request.POST['table']
        print(table)
        print('----')
        id = request.POST['id']
        
        if table == 'Counter':
            counter_title = request.POST['counter_title']
            counter_desc = request.POST['counter_desc']
            counter_subtitle = request.POST['counter_subtitle']
            counter_text1 = request.POST['counter_text1']
            counter_count1 = request.POST['counter_count1']
            
            counter_text2 = request.POST['counter_text2']
            counter_count2 = request.POST['counter_count2']
            
            counter_text3 = request.POST['counter_text3']
            counter_count3 = request.POST['counter_count3']
            
            counter_text4 = request.POST['counter_text4']
            counter_count4 = request.POST['counter_count4']
            
            counter_text5 = request.POST['counter_text5']
            counter_count5 = request.POST['counter_count5']
            
            counter_text6 = request.POST['counter_text6']
            counter_count6 = request.POST['counter_count6']
            data = Counter.objects.filter(pk=id).update(counter_title=counter_title,counter_desc=counter_desc,counter_subtitle=counter_subtitle,counter_text1=counter_text1,counter_count1=counter_count1,counter_text2=counter_text2,counter_count2=counter_count2,counter_text3=counter_text3,counter_count3=counter_count3,counter_text4=counter_text4,counter_count4=counter_count4,counter_text5=counter_text5,counter_count5=counter_count5,counter_text6=counter_text6,counter_count6=counter_count6)
        return redirect('website:dashboard')

    def get(self,request,website=None,page=None):
        #type like torque.domain.com/home
        website_url=website
        page_url=page
        website = Website.objects.get(website_url=website_url)
        page = Page.objects.get(page_url=page_url) #add page_url in model
        all_pages = Page.objects.filter(page_website_id=website)
        #pageDiv = PageDiv.objects.filter(page_div_page_id=page)
        pageElement = PageElement.objects.filter(page_element_page_id_id=page.pk)
        print(pageElement)
        #meta data
        meta = Meta.objects.filter(meta_website_id=website.pk)
        
        #header data
        header = Header.objects.get(header_website_id=website.pk)
        menu1 = Menu1.objects.filter(menu1_header_id=header.pk).order_by("menu1_order")
        menu_data = [{}]*menu1.count()
        
        print('-------menu1-----')
        print(menu1)
        for index,each1 in enumerate(menu1):
            print(each1.menu1_title)
            menu_data[index] = {'order':each1.menu1_order}
            menu_data[index]['id'] = each1.id
            menu_data[index]['title'] = each1.menu1_title
            menu_data[index]['link_type'] = each1.menu1_link_type
            menu_data[index]['link_url'] = each1.menu1_link_url
            menu_data[index]['is_active'] = each1.menu1_is_active
            
            menu2 = Menu2.objects.filter(menu2_menu1_id=each1.pk).order_by("menu2_order")
            menu_data[index]['childs'] = menu2
             
            print('----------------Menu2----------------')
            print(menu2)
        
        print('final data----------------')
        print(menu_data)

        page_data = [{}]*pageElement.count()
        #div_data = [{}]*pageDiv.count()

        for idx,each_pageElement in enumerate(pageElement):
            print(each_pageElement.page_element_table + ' - '+str(each_pageElement.page_element_table_id))
            page_data[idx] = {'order':each_pageElement.page_element_order}
            #div_data[idx] = {'order':each_pageDiv.page_div_order}
            #elementData = DivData.objects.filter(div_data_page_div_id_id=each_pageDiv)
            #for each_divData in divData:
            #    elementType = ElementType.objects.filter(element_type_divData_id=each_divData)
            #    for each_elementType in elementType:
            page_data[idx]['id'] = each_pageElement.pk
            page_data[idx]['file'] = each_pageElement.page_element_file+'Edit.html'
            page_data[idx]['type'] = each_pageElement.page_element_table
            #div_data[idx]['type'] = each_elementType.element_type_table
                    
            if each_pageElement.page_element_table == 'counter':
                elementData = Counter.objects.filter(pk=each_pageElement.page_element_table_id)
                #elementStyle = CounterStyle.objects.filter(id=elementData[0].counter_data_style_id)
                #print(elementData[0].counter_text1)
                page_data[idx]['data'] = elementData.values()
                #for each_elementData in elementData:
                 #   div_data[idx]['data'] = elementData.values()
                 #   div_data[idx]['style'] = elementStyle.values()

            elif each_elementType.element_type_table == 'Review':
                elementData = ReviewData.objects.filter(review_data_element_id=each_elementType)
                elementStyle = ReviewStyle.objects.filter(id=elementData[0].review_data_style_id)
                div_data[idx]['data'] = elementData.values()
                div_data[idx]['style'] = elementStyle.values()
                

            else:
                pass

        ############################################
        # PAGE DIV 
        ############################################

        def sort_page(page_data):
            return page_data.get('order')

        page_data.sort(key=sort_page)

        #print(page_data)
        ##########################################
        # PAGE DIV DATA
        #########################################
        
        # def sort_div(div_data):
        #     return div_data.get('order')

        # div_data.sort(key=sort_div)
        # print(len(div_data))
        # print(div_data)
        return render(request,'porto/pages/editor.html',{'page_data':page_data,'website':website,'all_pages':all_pages,'page':page,'header':header,'menu1':menu1, 'menu_data':menu_data,'meta':meta})
     

class MasterView(View):
    def post(self,request):
        table = request.POST['table']
        print(table)
        print('----')
        id = request.POST['id']
        
        if table == 'Counter':
            counter_title = request.POST['counter_title']
            counter_desc = request.POST['counter_desc']
            counter_subtitle = request.POST['counter_subtitle']
            counter_text1 = request.POST['counter_text1']
            counter_count1 = request.POST['counter_count1']
            
            counter_text2 = request.POST['counter_text2']
            counter_count2 = request.POST['counter_count2']
            
            counter_text3 = request.POST['counter_text3']
            counter_count3 = request.POST['counter_count3']
            
            counter_text4 = request.POST['counter_text4']
            counter_count4 = request.POST['counter_count4']
            
            counter_text5 = request.POST['counter_text5']
            counter_count5 = request.POST['counter_count5']
            
            counter_text6 = request.POST['counter_text6']
            counter_count6 = request.POST['counter_count6']
            data = Counter.objects.filter(pk=id).update(counter_title=counter_title,counter_desc=counter_desc,counter_subtitle=counter_subtitle,counter_text1=counter_text1,counter_count1=counter_count1,counter_text2=counter_text2,counter_count2=counter_count2,counter_text3=counter_text3,counter_count3=counter_count3,counter_text4=counter_text4,counter_count4=counter_count4,counter_text5=counter_text5,counter_count5=counter_count5,counter_text6=counter_text6,counter_count6=counter_count6)
        return redirect('website:dashboard')

    def get(self,request,website=None,page=None):
        #type like torque.domain.com/home
        
        website_url=website
        page_url=page

        website = Website.objects.get(website_url=website_url)

        if(page==None):
            page = Page.objects.get(pk=website.website_homepage_id) #add page_url in model
        else:
            page = Page.objects.get(page_url=page_url)
        all_pages = Page.objects.filter(page_website_id=website)
        #header data
        header = Header.objects.get(header_website_id=website.pk)
        menu1 = Menu1.objects.filter(menu1_header_id=header.pk).order_by("menu1_order")
        menu_data = [{}]*menu1.count()
        
        print('-------menu1-----')
        print(menu1)
        for index,each1 in enumerate(menu1):
            print(each1.menu1_title)
            menu_data[index] = {'order':each1.menu1_order}
            menu_data[index]['id'] = each1.id
            menu_data[index]['title'] = each1.menu1_title
            menu_data[index]['link_type'] = each1.menu1_link_type
            menu_data[index]['link_url'] = each1.menu1_link_url
            menu_data[index]['is_active'] = each1.menu1_is_active
            
            menu2 = Menu2.objects.filter(menu2_menu1_id=each1.pk).order_by("menu2_order")
            menu_data[index]['childs'] = menu2
             
            print('----------------Menu2----------------')
            print(menu2)
        
        print('final data----------------')
        print(menu_data)

        #pageDiv = PageDiv.objects.filter(page_div_page_id=page)
        pageElement = PageElement.objects.filter(page_element_page_id_id=page.pk)
        print(pageElement)

        page_data = [{}]*pageElement.count()
        #div_data = [{}]*pageDiv.count()

        for idx,each_pageElement in enumerate(pageElement):
            print(each_pageElement.page_element_table + ' - '+str(each_pageElement.page_element_table_id))
            page_data[idx] = {'order':each_pageElement.page_element_order}
            #div_data[idx] = {'order':each_pageDiv.page_div_order}
            #elementData = DivData.objects.filter(div_data_page_div_id_id=each_pageDiv)
            #for each_divData in divData:
            #    elementType = ElementType.objects.filter(element_type_divData_id=each_divData)
            #    for each_elementType in elementType:
            page_data[idx]['id'] = each_pageElement.pk
            page_data[idx]['file'] = each_pageElement.page_element_file+'.html'
            page_data[idx]['type'] = each_pageElement.page_element_table
            #div_data[idx]['type'] = each_elementType.element_type_table
                    
            if each_pageElement.page_element_table == 'counter':
                elementData = Counter.objects.filter(pk=each_pageElement.page_element_table_id)
                #elementStyle = CounterStyle.objects.filter(id=elementData[0].counter_data_style_id)
                print(elementData[0].counter_text1)
                page_data[idx]['data'] = elementData.values()
                #for each_elementData in elementData:
                 #   div_data[idx]['data'] = elementData.values()
                 #   div_data[idx]['style'] = elementStyle.values()

            elif each_elementType.element_type_table == 'Review':
                elementData = ReviewData.objects.filter(review_data_element_id=each_elementType)
                elementStyle = ReviewStyle.objects.filter(id=elementData[0].review_data_style_id)
                div_data[idx]['data'] = elementData.values()
                div_data[idx]['style'] = elementStyle.values()
                

            else:
                pass

        ############################################
        # PAGE DIV 
        ############################################

        def sort_page(page_data):
            return page_data.get('order')

        page_data.sort(key=sort_page)

        #print(page_data)
        ##########################################
        # PAGE DIV DATA
        #########################################
        
        # def sort_div(div_data):
        #     return div_data.get('order')

        # div_data.sort(key=sort_div)
        # print(len(div_data))
        # print(div_data)
        return render(request,'porto/pages/index.html',{'page_data':page_data,'website':website,'all_pages':all_pages,'page':page,'menu_data':menu_data,'header':header})

class AddPage(View):
    def post(self,request):
        website_id = request.POST['website']
        #page_name = request.POST['name']
        page_url = request.POST['url']
        #page_title = request.POST['title']
        #page_desc = request.POST['desc']
        #page_author = request.POST['author']
        
        page = Page.objects.create(page_website_id_id=website_id, page_url=page_url)
        page.save()
        return redirect('edit/torquecc/'+page_url)

    def get(self,request,website,page):
        website_data = Website.objects.filter(website_url=website)
        return render(request,'porto/pages/editor.html',{'website':website,'page':{'order':1,'file':'counter.html'},'website_data':website_data})


class AddElement(View):
    def post(self,request):
        print('yes inside add--------------')
        page_id = request.POST['page']
        pos_after = int(request.POST['pos_after'])
        element_type = request.POST['element_type']
        element_file = request.POST['element_file']


        page = Page.objects.get(pk=page_id)
        website = Website.objects.get(pk=page.page_website_id.pk)
        
        if(element_type == 'counter'):
            counter = Counter.objects.create(counter_title="Our Achievements",counter_desc = "We were in field since last 10+ years", counter_number = "4",counter_icon1= '<i class="fa fa-smile-o" aria-hidden="true"></i>', counter_text1 = "Happy Clients", counter_count1_prepend = "", counter_count1 = "40000" , counter_count1_append = "+" ,counter_icon2 = '<i class="fa fa-clock-o" aria-hidden="true"></i>' , counter_text2 = "Years in Business", counter_count2_prepend = "", counter_count2 = "10", counter_count2_append = "+",counter_icon3 = '<i class="fa fa-coffee" aria-hidden="true"></i>' , counter_text3 = "Cups of Coffee", counter_count3_prepend = "", counter_count3 = "5000", counter_count3_append = "",counter_icon4 = '<i class="fa fa-money" aria-hidden="true"></i>' , counter_text4 = "Revenue", counter_count4_prepend = "", counter_count4 = "2", counter_count4_append = "M",counter_is_active= 1 ,counter_bg_image="", counter_bg_color = "#ffffff", counter_icon_color = "#000000", counter_title_color = "#000000", counter_text_color="#000000", counter_animation_type="",counter_animation_delay="0", counter_status = "Active", counter_created_date = datetime.now(), counter_updated_date = datetime.now())
            counter.save()
            
            elements = PageElement.objects.filter(page_element_page_id=page_id,page_element_order__gt=pos_after)
            print('---------------increase----------------')
            print(elements)
            for each in elements:
                each.page_element_order+=1
                each.save()
            
            element = PageElement.objects.create(page_element_table=element_type,page_element_table_id=counter.pk,page_element_order=pos_after+1,page_element_file=element_file,page_element_page_id_id=page_id)
            element.save()
            
            return redirect('edit/'+website.website_url+'/'+page.page_url)
        else:
            return redirect('dashboard')
        
    def get(self,request,website,page):
        website_data = Website.objects.filter(website_url=website)
        return render(request,'porto/pages/editor.html',{'website':website,'page':{'order':1,'file':'counter.html'},'website_data':website_data})

class RemoveElement(View):
    def post(self,request):
        page_id = request.POST['page_id']
        element_id = request.POST['id']
        
        page = Page.objects.get(pk=page_id)
        website = Website.objects.get(pk=page.page_website_id.pk)

        element = PageElement.objects.filter(pk=element_id)
        element_table = element[0].page_element_table
        element_table_id = element[0].page_element_table_id
        element_position = element[0].page_element_order

        elements = PageElement.objects.filter(page_element_page_id=page_id,page_element_order__gt=element_position)
        
        if(element_table == 'counter'):
            counter = Counter.objects.get(pk=element_table_id)
            counter.delete()

            elementDelete = PageElement.objects.get(pk=element_id)
            elementDelete.delete()

            for each in elements:
                each.page_element_order-=1
                each.save()
            return redirect('edit/'+website.website_url+'/'+page.page_url)
        else:
            print('nooooo')
            return redirect('website:dashboard')
        
    def get(self,request,website,page):
        website_data = Website.objects.filter(website_url=website)
        return render(request,'porto/pages/editor.html',{'website':website,'page':{'order':1,'file':'counter.html'},'website_data':website_data})


class UpDownElement(View):
    def post(self,request):
        page_id = request.POST['page_id']
        element_id = request.POST['id']
        action_type = request.POST['type']

        page = Page.objects.get(pk=page_id)
        website = Website.objects.get(pk=page.page_website_id.pk)

        element = PageElement.objects.filter(pk=element_id)
        element_position = element[0].page_element_order
        print('inside updown')
        if(action_type == 'up'):
            element2 =  PageElement.objects.filter(page_element_page_id=page_id,page_element_order=element_position-1)
            elementSecond = element2[0]
            elementSecond.page_element_order+=1
            elementSecond.save()
            elementFirst = element[0]
            elementFirst.page_element_order -=1
            elementFirst.save()
            return redirect('edit/'+website.website_url+'/'+page.page_url)
        elif(action_type == 'down'):
            element2 =  PageElement.objects.filter(page_element_page_id=page_id,page_element_order=element_position+1)
            elementSecond = element2[0]
            elementSecond.page_element_order-=1
            elementSecond.save()
            elementFirst = element[0]
            elementFirst.page_element_order +=1
            elementFirst.save()
            return redirect('edit/'+website.website_url+'/'+page.page_url)
        else:
            print('nooooo')
            return redirect('website:dashboard')
        
    def get(self,request,website,page):
        website_data = Website.objects.filter(website_url=website)
        return render(request,'porto/pages/editor.html',{'website':website,'page':{'order':1,'file':'counter.html'},'website_data':website_data})

class EditElement(View):
    def post(self,request):
        table = request.POST['table']
        print(table)
        print('----')
        id = request.POST['id']
        bg_available = request.GET.get('bg')
        animation = request.GET.get('animation')
        
        if table == 'counter':
            
            counter_title = request.POST['counter_title']
            counter_desc = request.POST['counter_desc']
            counter_number = request.POST['counter_number']

            counter_icon1 = request.POST['counter_icon1']
            counter_text1 = request.POST['counter_text1']
            counter_1_prepend = request.POST['counter_1_prepend']
            counter_1_number = request.POST['counter_1_number']
            counter_1_append = request.POST['counter_1_append']
            
            counter_icon2 = request.POST['counter_icon2']
            counter_text2 = request.POST['counter_text2']
            counter_2_prepend = request.POST['counter_2_prepend']
            counter_2_number = request.POST['counter_2_number']
            counter_2_append = request.POST['counter_2_append']

            counter_icon3 = request.POST['counter_icon3']
            counter_text3 = request.POST['counter_text3']
            counter_3_prepend = request.POST['counter_3_prepend']
            counter_3_number = request.POST['counter_3_number']
            counter_3_append = request.POST['counter_3_append']
                        
            counter_icon4 = request.POST['counter_icon4']
            counter_text4 = request.POST['counter_text4']
            counter_4_prepend = request.POST['counter_4_prepend']
            counter_4_number = request.POST['counter_4_number']
            counter_4_append = request.POST['counter_4_append']
            
            counter_bg_image = request.POST['counter_bg_image']
            
            if (bg_available == "yes"):
                print('uploading')
                section_background = request.FILES.get('1_image',0)
                #section_background = request.FILES['1_image']
                
                print(section_background)
                if(section_background != 0):

                    fs = FileSystemStorage(location='media/counter/')
                    name = fs.save(time.strftime("%Y%m%d_%H%M%S")+".png",section_background)
                    counter_bg_image = fs.url(name)

                    update_bg = Counter.objects.filter(pk=id).update(counter_bg_image = counter_bg_image)           

            if (animation == "yes"):

                animation_type = request.POST.get('animation_type',0)
                animation_delay = request.POST.get('animation_delay',0)

                
                update_animation_data = Counter.objects.filter(pk=id).update(counter_animation_type = animation_type, counter_animation_delay=animation_delay)
                
            background_color_value = request.POST['background_color_value']
            title_color_value = request.POST['title_color_value']
            counter_icon_color_value = request.POST['counter_icon_color_value']
            counter_text_color_value = request.POST['counter_text_color_value']

            
            data = Counter.objects.filter(pk=id).update(counter_title=counter_title,counter_desc = counter_desc, counter_number = counter_number,counter_icon1= counter_icon1, counter_text1 = counter_text1, counter_count1_prepend = counter_1_prepend, counter_count1 = counter_1_number , counter_count1_append = counter_1_append ,counter_icon2 = counter_icon2 , counter_text2 = counter_text2, counter_count2_prepend = counter_2_prepend, counter_count2 = counter_2_number, counter_count2_append = counter_2_append,counter_icon3 = counter_icon3 , counter_text3 = counter_text3, counter_count3_prepend = counter_3_prepend, counter_count3 = counter_3_number, counter_count3_append = counter_3_append,counter_icon4 = counter_icon4 , counter_text4 = counter_text4, counter_count4_prepend = counter_4_prepend, counter_count4 = counter_4_number, counter_count4_append = counter_4_append, counter_bg_color = background_color_value , counter_icon_color = counter_icon_color_value, counter_title_color = title_color_value, counter_text_color = counter_text_color_value, counter_updated_date = datetime.now())

            return redirect('website:dashboard')

        

        return redirect('website:dashboard')

    def get(self,request):
        return redirect('website:dashboard')

    
class EditMeta(View):
    def post(self,request):
        if 'retarget_code_submit' in request.POST:
            
            website_id = request.POST['website_id']
            
            fb_retargetting_pixel = "<!--<!--" + request.POST['fb_retargetting_pixel'] + "-->-->"
            perfect_audience_pixel = "<!--<!--" +request.POST['perfect_audience_pixel'] + "-->-->"
            google_analytics = "<!--<!--" + request.POST['google_analytics'] + "-->-->"

            meta_data = Meta.objects.filter(meta_website_id= website_id)
           
            
           
            print(meta_data)
            if(meta_data.count() > 0):
              
                newMeta = meta_data[0]
                newMeta.meta_in_head_content = fb_retargetting_pixel
                newMeta.meta_begin_body_content = perfect_audience_pixel
                newMeta.meta_end_body_content = google_analytics
               
                newMeta.save()
            else:
                website = Meta.objects.create(meta_in_head_content=fb_retargetting_pixel, meta_begin_body_content=perfect_audience_pixel,meta_end_body_content=google_analytics, meta_is_active = '1' , meta_created_date = datetime.now(),meta_updated_date=datetime.now(),meta_website_id_id = website_id)
                website.save()
        return redirect('website:dashboard')

    def get(self,request):
        return redirect('website:dashboard')
    

class EditHeader(View):
    def post(self,request):  
        if 'website' in request.POST:
            website_id = request.POST['website']
            header = Header.objects.get(header_website_id_id=website_id)

        if 'add_header_details' in request.POST:
            header.header_contact = request.POST['header_contact']
            header.header_email = request.POST['header_email']
            header.header_facebook = request.POST['header_facebook']
            header.header_twitter = request.POST['header_twitter']
            header.header_instagram = request.POST['header_instagram']
            header.header_tagline = request.POST['header_tagline']
            header.save()
            return redirect('website:dashboard')

        elif 'change_header' in request.POST:
            header_id = request.POST['id']
            header_style = request.POST['header_style']+'.html'
            header = Header.objects.get(pk=header_id)
            header.header_file = header_style
            header.save()
            return redirect('website:dashboard')

        elif 'add_menu1' in request.POST:
            menu1Data = Menu1.objects.filter(menu1_header_id=header.pk).order_by("-menu1_order")[:1]
            print(menu1Data[0].menu1_order)

            menu1_title = request.POST['menu1_title']
            menu1_type = request.POST['menu1_type']
            if(menu1_type == 'external'):
                menu1_link_url = request.POST['menu1_link_url']
            elif(menu1_type == 'page'):
                menu1_link_url = request.POST['menu1_page_link']
            else:
                pass
            menu1 = Menu1.objects.create(menu1_title=menu1_title,menu1_order=int(menu1Data[0].menu1_order)+1,menu1_link_type=menu1_type,menu1_link_url=menu1_link_url,menu1_is_active=1,menu1_header_id_id=header.pk)
            return redirect('website:dashboard')
        elif 'add_menu2' in request.POST:
            menu1_id = request.POST['menu1_select']
            menu2_title = request.POST['menu2_title']
            menu2_type = request.POST['menu2_type']
            if(menu2_type == 'external'):
                menu2_link_url = request.POST['menu2_link_url']
            elif(menu2_type == 'page'):
                menu2_link_url = request.POST['menu2_page_link']
            else:
                pass
            
            menu2Data = Menu2.objects.filter(menu2_menu1_id_id=menu1_id).order_by("-menu2_order")[:1]
            if menu2Data.count() != 0:
                menu2Order = int(menu2Data[0].menu2_order) + 1
            else:
                menu2Order = 1
            menu2 = Menu2.objects.create(menu2_title=menu2_title,menu2_order=menu2Order,menu2_link_type=menu2_type,menu2_link_url=menu2_link_url,menu2_is_active=1,menu2_menu1_id_id=menu1_id)
            return redirect('website:dashboard')
    
        elif 'edit_menu1' in request.POST:
            menu1_id = request.POST['menu1_id']
            menu1_title = request.POST['menu1_title']
            menu1_link_type = request.POST['menu1_link_type']
            if(menu1_link_type == 'external'):
                menu1_link_url = request.POST['menu1_link_url']
            elif(menu1_link_type == 'page'):
                menu1_link_url = request.POST['menu1_page_link']
            else:
                pass
            
            menu1 = Menu1.objects.get(pk=int(menu1_id))
            menu1.menu1_title = menu1_title
            menu1.menu1_link_type = menu1_link_type
            menu1.menu1_link_url = menu1_link_url
            print(menu1.menu1_link_type)
            print('above!!!!!')
            menu1.save()
            return redirect('website:dashboard')
        elif 'edit_menu2' in request.POST:
            menu2_id = request.POST['menu2_id']
            menu2_title = request.POST['menu2_title']
            menu2_link_type = request.POST['menu2_link_type']
            if(menu2_link_type == 'external'):
                menu2_link_url = request.POST['menu2_link_url']
            elif(menu2_link_type == 'page'):
                menu2_link_url = request.POST['menu2_page_link']
            else:
                pass
            
            menu2 = Menu2.objects.get(pk=int(menu2_id))
            menu2.menu2_title = menu2_title
            menu2.menu2_link_type = menu2_link_type
            menu2.menu2_link_url = menu2_link_url
            
            menu2.save()
            return redirect('website:dashboard')
        elif 'removeMenu2' in request.POST:
            menu2_id = request.POST['menu2_id']
            menu2 = Menu2.objects.get(pk=int(menu2_id))
            order = menu2.menu2_order
            parent = menu2.menu2_menu1_id
            menu2.delete()
            menu2_data = Menu2.objects.filter(menu2_menu1_id=parent, menu2_order__gt=order)
            print('----menu2 grt----')
            print(menu2_data)
            for each in menu2_data:
                each.menu2_order-=1
                each.save()
            return redirect('website:dashboard')
        elif 'removeMenu1' in request.POST:
            menu1_id = request.POST['menu1_id']
            menu2 = Menu2.objects.filter(menu2_menu1_id=menu1_id)

            for each in menu2:
                each.delete()
            menu1 = Menu1.objects.get(pk=menu1_id)
            order = menu1.menu1_order
            parent = menu1.menu1_header_id
            menu1_data = Menu1.objects.filter(menu1_header_id=parent, menu1_order__gt=order)
            
            for each in menu1_data:
                each.menu1_order-=1
                each.save()
            menu1.delete()  
            return redirect('website:dashboard')
        else:
            pass

    def get(self,request):
        return redirect('website:dashboard')