from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404
from .models import GeneratedModel
from .services.model_generator import generate_json_model


# ---------------------------
# Form + Generator View
# ---------------------------
def create_model(request):
    if request.method == "POST":
        model = GeneratedModel.objects.create(
            name=request.POST['name'],
            model_type=request.POST['model_type'],
            width=request.POST['width'],
            height=request.POST['height'],
            depth=request.POST['depth']
        )

        filename, file_content = generate_json_model(model)
        model.output_file.save(filename, file_content)
        model.save()

        return redirect('create_model')

    return render(request, 'create_model.html')


# ---------------------------
# API View (STEP 5.2)
# ---------------------------
def model_detail_api(request, model_id):
    try:
        model = GeneratedModel.objects.get(id=model_id)
    except GeneratedModel.DoesNotExist:
        raise Http404("Model not found")

    data = {
        "id": model.id,
        "name": model.name,
        "type": model.model_type,
        "dimensions": {
            "width": model.width,
            "height": model.height,
            "depth": model.depth
        },
        "file_url": model.output_file.url if model.output_file else None,
        "created_at": model.created_at.isoformat()
    }

    return JsonResponse(data)

def model_viewer(request, model_id):
    return render(request, "viewer.html", {"model_id": model_id})

# views.py
from django.http import JsonResponse

# Simple template-based approach
OBJECTS = {
    "apple": {"type": "sphere", "color": "red", "size": 1},
    "cube": {"type": "cube", "color": "blue", "size": 1},
    "cylinder": {"type": "cylinder", "color": "green", "size": 1}
}

def generate_object(request):
    name = request.GET.get('name', '').lower()
    obj_data = OBJECTS.get(name)
    if obj_data:
        return JsonResponse(obj_data)
    return JsonResponse({"error": "Object not found"}, status=404)


