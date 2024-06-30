from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from streamapp.camera import VideoCamera

# from django.http import HttpResponse
# from matplotlib import pylab
# from pylab import *
# import PIL, PIL.Image, StringIO

# Create your views here.


def index(request):
    return render(request, "streamapp/home.html")


def main(request):
    return render(request, "streamapp/mainhome.html")


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n")


def video_feed(request):
    return StreamingHttpResponse(
        gen(VideoCamera()), content_type="multipart/x-mixed-replace; boundary=frame"
    )


# def anal(request):
#     x = VideoCamera().get_arr()
#     s = range(1, 10)
#     plot(x, s)

#     xlabel("xlabel(X)")
#     ylabel("ylabel(Y)")
#     title("Simple Graph!")
#     grid(True)

#     # Store image in a string buffer
#     buffer = StringIO.StringIO()
#     canvas = pylab.get_current_fig_manager().canvas
#     canvas.draw()
#     pilImage = PIL.Image.fromstring(
#         "RGB", canvas.get_width_height(), canvas.tostring_rgb()
#     )
#     pilImage.save(buffer, "PNG")
#     pylab.close()

#     # Send buffer in a http response the the browser with the mime type image/png set
#     return HttpResponse(buffer.getvalue(), mimetype="image/png")


def anal(request):
    # ... your logic to get the array ...
    my_array = VideoCamera().get_arr()
    context = {"my_array": my_array}
    return render(request, "streamapp/extra.html", context)
