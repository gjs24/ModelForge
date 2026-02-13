from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404
from .models import GeneratedModel
from .services.model_generator import generate_json_model


OBJECTS = {
    "apple": {
        "type": "sphere",
        "color": "#ff0000",
        "size": 1
    },
    "cube": {
        "type": "cube",
        "color": "#0000ff",
        "size": 1
    },
}

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
    "color": json.loads(model.output_file.read().decode()).get("color", "#38bdf8"),
    "dimensions": {
        "width": model.width,
        "height": model.height,
        "depth": model.depth
    },
    "file_url": model.output_file.url if model.output_file else None,
}


    return JsonResponse(data)

def model_viewer(request, model_id):
    return render(request, "viewer.html", {"model_id": model_id})

from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
import json


def parse_prompt(prompt):
    words = prompt.lower().split()

    size_multiplier = 1
    color = "#38bdf8"
    object_name = None

    # Size detection
    if "big" in words:
        size_multiplier = 2
    elif "small" in words:
        size_multiplier = 0.5
    elif "medium" in words:
        size_multiplier = 1

    # Color detection
    colors = {
        "red": "#ff0000",
        "green": "#00ff00",
        "blue": "#0000ff",
        "yellow": "#ffff00",
        "purple": "#800080",
        "black": "#000000",
        "white": "#ffffff",
    }

    for word in words:
        if word in colors:
            color = colors[word]

    # Object detection
    for obj in OBJECTS.keys():
        if obj in words:
            object_name = obj
            break

    return object_name, size_multiplier, color

@csrf_exempt
def generate_object(request):
    prompt = request.GET.get('name', '').lower()

    if not prompt:
        return JsonResponse({"error": "No prompt provided"}, status=400)

    object_name, size_multiplier, color = parse_prompt(prompt)

    if not object_name:
        return JsonResponse({"error": "Object not recognized"}, status=400)

    base_object = OBJECTS.get(object_name)

    if not base_object:
        return JsonResponse({"error": "Object not supported"}, status=400)

    # Apply size multiplier
    width = base_object["size"] * size_multiplier
    height = base_object["size"] * size_multiplier
    depth = base_object["size"] * size_multiplier

    # Create DB entry
    model = GeneratedModel.objects.create(
        name=prompt,
        model_type=base_object["type"],
        width=width,
        height=height,
        depth=depth
    )

    # Create JSON file
    json_data = json.dumps({
        "type": base_object["type"],
        "color": color,
        "size": size_multiplier
    })

    file_content = ContentFile(json_data.encode('utf-8'))
    filename = f"{object_name}_{model.id}.json"

    model.output_file.save(filename, file_content)
    model.save()

    return JsonResponse({
        "success": True,
        "model_id": model.id
    })
