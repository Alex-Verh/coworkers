from django.views import generic
from django.shortcuts import get_object_or_404, redirect
from .models import CustomUser, WorkerLanguage, WorkerNationality, Trait, WorkerTrait, Language, Nationality, Experience
from django.db.models import OuterRef, Subquery, IntegerField, Value, Q, F
from django.db.models.functions import Coalesce
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from .forms import CustomUserCreationForm, ExperienceForm, ContactForm, FullNameUpdateForm, SalaryUpdateForm, LocationUpdateForm, PfpForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.generic.edit import FormView, View
from .mixins import ExperienceFormMixin, ContactFormMixin
from django.core.mail import EmailMessage
import json
import os
from django.conf import settings
from django.core.exceptions import ValidationError


class IndexView(generic.ListView, ContactFormMixin):
    template_name = "index.html"
    context_object_name = 'users'
    paginate_by = 3

    def get_queryset(self):
        return CustomUser.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users_section'] = self.get_queryset()[:6]  # first section
        return context

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                page_number = int(request.GET.get('page', 1))
            except ValueError:
                return JsonResponse({"error": "Invalid page number."}, status=400)

            worker_query = request.GET.get('worker', '').strip()
            location_query = request.GET.get('location', '').strip()
            experience_query = request.GET.get('experience', None)
            language_query = request.GET.get('language', '').strip()
            salary_query = request.GET.get('salary', None)

            filters = Q()

            if worker_query:
                filters &= Q(experiences__type='Work') & Q(experiences__position__icontains=worker_query)

            if location_query:
                filters &= Q(location__icontains=location_query)

            if language_query:
                try:
                    language_ids = [int(lang_id) for lang_id in language_query.split(",")]
                    filters &= Q(workerlanguage__language_id__in=language_ids)
                except ValueError:
                    return JsonResponse({"error": "Invalid language filter format."}, status=400)

            if experience_query:
                try:
                    experience_ranges = experience_query.split(",")
                    experience_filters = Q()
                    for experience_range in experience_ranges:
                        min_experience, max_experience = experience_range.split("-")
                        min_experience = int(min_experience)

                        if max_experience == "inf":
                            experience_filters |= Q(experience__gte=min_experience)
                        else:
                            max_experience = int(max_experience)
                            experience_filters |= Q(experience__gte=min_experience, experience__lte=max_experience)

                    filters &= experience_filters
                except (ValueError, AttributeError):
                    return JsonResponse({"error": "Invalid experience filter format."}, status=400)

            if salary_query:
                try:
                    salary_ranges = salary_query.split(",")
                    salary_filters = Q()
                    for salary_range in salary_ranges:
                        min_salary, max_salary = salary_range.split("-")
                        min_salary = int(min_salary) * 1000

                        if max_salary == "inf":
                            salary_filters |= Q(salary_minimum__gte=min_salary)
                        else:
                            max_salary = int(max_salary) * 1000
                            salary_filters |= Q(salary_minimum__gte=min_salary, salary_minimum__lte=max_salary)

                    filters &= salary_filters
                except (ValueError, AttributeError):
                    return JsonResponse({"error": "Invalid salary filter format."}, status=400)

            try:
                queryset = CustomUser.objects.filter(filters).order_by('id').distinct()
            except ValidationError as e:
                return JsonResponse({"error": f"Invalid query: {e.message}"}, status=400)

            paginator = Paginator(queryset, 3)
            try:
                page_obj = paginator.get_page(page_number)
            except Exception as e:
                return JsonResponse({"error": "Error in pagination."}, status=400)

            users_data = [
                {
                    "id": user.id,
                    "full_name": user.full_name,
                    "position": user.position,
                    "experience": user.experience,
                    "description": user.description,
                }
                for user in page_obj
            ]

            return JsonResponse({
                "users": users_data,
                "has_next": page_obj.has_next()
            })

        return super().get(request, *args, **kwargs)
    

class ProfileView(LoginRequiredMixin, ExperienceFormMixin, ContactFormMixin,  generic.DetailView):
    model = CustomUser
    template_name = "profile.html"
    context_object_name = 'worker'

    def get_object(self, queryset=None):
        """Retrieve the user object based on the URL or the logged-in user."""
        if 'pk' in self.kwargs:
            return get_object_or_404(CustomUser, pk=self.kwargs['pk'])
        else:
            return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()

        section = self.request.GET.get("section", "personal-data")

        user_languages = WorkerLanguage.objects.filter(user=user).select_related('language')
       
        user_nationalities = WorkerNationality.objects.filter(user=user).select_related('nationality')

        user_trait_measure  = WorkerTrait.objects.filter(
        user=user,
        trait=OuterRef('pk')
        ).values('trait_measure')[:1]

        personal_attributes = Trait.objects.annotate(
            user_score=Coalesce(Subquery(user_trait_measure, output_field=IntegerField()), Value(1))
        )

        # forms
        context['full_name_form'] = FullNameUpdateForm(instance=user)
        context['salary_form'] = SalaryUpdateForm(instance=user)
        context['location_form'] = LocationUpdateForm(instance=user)
        context['pfp_form'] = PfpForm(instance=user)

        # other context data
        context['is_own_profile'] = (user == self.request.user)
        context['formatted_salary_minimum'] = user.formatted_salary(user.salary_minimum)
        context['formatted_salary_maximum'] = user.formatted_salary(user.salary_maximum)

        experiences = sorted(
            user.experiences.all(),
            key=lambda x: (x.end_year is not None, -x.end_year if x.end_year is not None else float('inf'))
        )        
        context['experiences'] = experiences

        context['languages'] = user_languages
        context['nationalities'] = user_nationalities
        context['traits'] = personal_attributes
        context['section'] = section

        return context
    
    def post(self, request, *args, **kwargs):
        user = self.get_object()
        if 'full_name_form' in request.POST:
            form = FullNameUpdateForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "Full name updated successfully!")
            else:
                messages.error(request, "There was an error updating your full name.")

        elif 'salary_form' in request.POST:
            form = SalaryUpdateForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "Salary preference updated successfully!")
            else:
                messages.error(request, "There was an error updating your salary preference.")

        elif 'location_form' in request.POST:
            form = LocationUpdateForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "Current location updated successfully!")
            else:
                messages.error(request, "There was an error updating your current location.")

        elif 'pfp_form' in request.POST:
            form = PfpForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                if user.profile_picture:
                    old_picture_path = user.profile_picture.path
                    if os.path.exists(old_picture_path):
                        os.remove(old_picture_path)

                form.save()
                return JsonResponse({'message' : f'Profile picture has been updated successfully.', 'url': user.profile_picture.url})
            else:
                return JsonResponse({"errors": "Problem while updating the profile picture.", "status": "error"}, status=400)

        return redirect('my_profile')
    
    
class RegisterView(generic.FormView, ContactFormMixin):
    template_name = "register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    

    def form_valid(self, form):
        try:
            user = form.save(commit=False)

            country = form.cleaned_data.get('location_country')
            city = form.cleaned_data.get('location_city')
            user.location = ", ".join(filter(None, [city, country]))

            user.save()

            user_name = form.cleaned_data.get('full_name')
            messages.success(self.request, f'Account has been created. Good luck, {user_name}!')
        except Exception as e:
            messages.error(self.request, f"An error occurred while creating your account: {e}")
            return self.form_invalid(form)
        
        return super().form_valid(form)
    

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                readable_field = field.capitalize().replace("_", " ")

                messages.error(self.request, f"{readable_field}: {error}")
        return super().form_invalid(form)
    

class ExperienceView(LoginRequiredMixin, FormView):
    form_class = ExperienceForm

class ExperienceView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        experience_id = kwargs.get("experience_id")
        experience = get_object_or_404(Experience, experience_id=experience_id, user=request.user)
        data = {
            "experience_id": experience.experience_id,
            "position": experience.position,
            "institution_name": experience.institution_name,
            "description": experience.description,
            "start_year": experience.start_year,
            "end_year": experience.end_year,
            "type": experience.type,
        }
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.user = request.user
            experience_type = experience.type.lower()
            experience.save()
            messages.success(self.request, f'Experience added successfully!')
            return redirect(f'{reverse("my_profile")}?section={experience_type}-timeline')
        else:
            return JsonResponse({"errors": form.errors}, status=400)


    def patch(self, request, *args, **kwargs):
        experience_id = kwargs.get("experience_id")
        experience = get_object_or_404(Experience, experience_id=experience_id, user=request.user)

        if request.content_type == "application/json":
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"errors": "Invalid JSON data.", "status": "error"}, status=400)
        else:
            data = request.POST

        form = ExperienceForm(data, instance=experience)
        if form.is_valid():
            form.save()
            experience_position = experience.position
            return JsonResponse({'message' : f'Experience "{experience_position}" has been updated successfully.'}, status=200)
        
        print(form.errors)
        return JsonResponse({"errors": form.errors, "status": "error"}, status=400)
    
    def delete(self, request, *args, **kwargs):
        try:
            experience_id = kwargs.get("experience_id")

            if not experience_id:
                return JsonResponse({'error': 'Experience ID is required.'}, status=400)

            experience = Experience.objects.get(experience_id=experience_id)
            experience_position = experience.position

            experience.delete()

            return JsonResponse({'message' : f'Experience "{experience_position}" has been updated successfully.'}, status=200)

        except Exception:
            return JsonResponse({'error': 'Couldn\'t delete the experience record.'}, status=404)
    
    
class WorkerTraitView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user

        data = json.loads(request.body)
        trait_id = data.get('trait_id')
        trait_score = data.get('trait_score')

        if not trait_id or not trait_score:
            return JsonResponse({'messages': ['Trait ID and score are required.']}, status=400)

        try:
            trait = Trait.objects.get(trait_id=trait_id) 
        except Trait.DoesNotExist:
            return JsonResponse({'messages': ['Trait not found.']}, status=404)

        try:
            _, created = WorkerTrait.objects.update_or_create(
                user=user,
                trait=trait,
                defaults={'trait_measure': trait_score},
            )
            if created:
                return JsonResponse({'messages': [f"Trait \"{trait.trait_name.strip()}\" added with score {trait_score}."]})
            else:
                return JsonResponse({'messages': [f"Trait \"{trait.trait_name.strip()}\" updated with score {trait_score}."]})
        except Exception as e:
            return JsonResponse({'messages': [f"An error occurred: {e}"]}, status=500)


class ContactView(FormView):
    template_name = "contact_form.html" 
    form_class = ContactForm
    success_url = reverse_lazy('index')  

    def form_valid(self, form):
        message = form.cleaned_data['contact']
        
        email = EmailMessage(
            subject="Contact Form Submission",
            body=message,
            from_email="anonym@user.com",
            to=[settings.EMAIL_HOST], 
        )
        try:
            email.send() 
            messages.success(self.request, "Your message has been sent successfully.")
        except Exception as e:
            messages.error(self.request, f"Failed to send the message: {e}")
        
        return super().form_valid(form)
    

class LanguageView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.path.endswith('own/'):
            return self.get_own(request, *args, **kwargs)
        else:
            return self.search_languages(request, *args, **kwargs)

    def search_languages(self, request, *args, **kwargs):
        query = request.GET.get('name', '').strip().lower()
        results = Language.objects.filter(language_name__icontains=query)

        results_data = [
            {
                'language_id': result.language_id,
                'language_name': result.language_name,
            }
            for result in results
        ]

        if not results_data:
            return JsonResponse({'message': f'No languages found for this query.'}, status=200)

        return JsonResponse({'results': results_data}, status=200)
    
    def get_own(self, request, *args, **kwargs):
        try:
            results = WorkerLanguage.objects.filter(user=request.user)
            
            if not results.exists():
                return JsonResponse({'results': []}, status=200)

            results = [
                {
                    'language_id': result.language.language_id,
                    'language_name': result.language.language_name,
                }
                for result in results
            ]

            return JsonResponse({'results': results}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            language_id = data.get('language_id')

            if not language_id:
                return JsonResponse({'error': 'Language ID is required.'}, status=400)

            language = Language.objects.get(language_id=language_id)
            WorkerLanguage.objects.create(user=request.user, language=language)

            return JsonResponse({'message': f'Language "{language.language_name}" added successfully.'}, status=201)
        except Language.DoesNotExist:
            return JsonResponse({'error': 'Language not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def delete(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            language_id = data.get('language_id')

            if not language_id:
                return JsonResponse({'error': 'Language ID is required.'}, status=400)

            language = Language.objects.get(language_id=language_id)
            WorkerLanguage.objects.filter(user=request.user, language_id=language_id).delete()

            return JsonResponse({'message': f'Language "{language.language_name}" removed successfully.'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    

class NationalityView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.path.endswith('own/'):
            return self.get_own(request, *args, **kwargs)
        else:
            return self.search_nationalities(request, *args, **kwargs)

    def search_nationalities(self, request, *args, **kwargs):
        query = request.GET.get('name', '').strip().lower()
        results = Nationality.objects.filter(nationality_name__icontains=query)

        results_data = [
            {
                'nationality_id': result.nationality_id,
                'nationality_name': result.nationality_name,
            }
            for result in results
        ]

        
        if not results_data:
            return JsonResponse({'message': f'No nationalities found for this query.'}, status=200)

        return JsonResponse({'results': results_data}, status=200)
    
    def get_own(self, request, *args, **kwargs):
        try:
            results = WorkerNationality.objects.filter(user=request.user)
            
            if not results.exists():
                return JsonResponse({'results': []}, status=200)


            results = [
                {
                    'nationality_id': result.nationality.nationality_id,
                    'nationality_name': result.nationality.nationality_name,
                }
                for result in results
            ]

            return JsonResponse({'results': results}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            nationality_id = data.get('nationality_id')

            if not nationality_id:
                return JsonResponse({'error': 'Nationality ID is required.'}, status=400)

            nationality = Nationality.objects.get(nationality_id=nationality_id)

            if WorkerNationality.objects.filter(user=request.user, nationality=nationality).exists():
                return JsonResponse({'error': f'Nationality "{nationality.nationality_name}" is already added.'}, status=400)

            WorkerNationality.objects.create(user=request.user, nationality=nationality)

            return JsonResponse({'message': f'Nationality "{nationality.nationality_name}" added successfully.'}, status=201)
        except Nationality.DoesNotExist:
            return JsonResponse({'error': 'Nationality not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def delete(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            nationality_id = data.get('nationality_id')

            if not nationality_id:
                return JsonResponse({'error': 'Nationality ID is required.'}, status=400)

            nationality = Nationality.objects.get(nationality_id=nationality_id)
            WorkerNationality.objects.filter(user=request.user, nationality_id=nationality_id).delete()

            return JsonResponse({'message': f'Nationality "{nationality.nationality_name}" removed successfully.'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)