#import asyncio
import psutil
import json
import modules.state as state
import modules.tasks as tasks

#background_tasks = set()
# ^ originally using asyncio, will not work anymore.

#update the CPU dictionary variable
def update_cpu_dict(self):
    print("Tracking.")
    while not state.mainFinished:
        state.cpudict["cpu_percent"] = psutil.cpu_percent()
        tasks.wait(1000)
    print("Update CPU dictionaries task ended.")
    return True


def print_dict(self):
    print("Starting.")
    tasks.wait(5000)
    while not state.mainFinished:
        prettyPrint = json.dumps(state.cpudict)
        print(prettyPrint)
        tasks.wait(1000)
    print("End.")
    return True
    #end

def prep_tasks(window):
    #test
    tasks.start(window, update_cpu_dict)
    tasks.start(window, print_dict)

    
    #that's it!  ez

def uri_to_embed(uri): 
    """
    <html>
        <script src=\"https://open.spotify.com/embed-podcast/iframe-api/v1\" async></script>
        <script>
            window.onSpotifyIframeApiReady = (IFrameAPI) => {
                const element = document.getElementById('embed-iframe');
                const options = {
                    uri: '[[URI]]'
                };
                const callback = (EmbedController) => {};
                IFrameAPI.createController(element, options, callback);
            };
        </script>
        <body> 
            <div id="embed-iframe"></div>
        </body> 
    </html>
    """
    rough = uri_to_embed.__doc__
    toWrite = rough.replace("[[URI]]", str(uri))
    path = "embed.html"
    with open(path, 'w') as html:
        html.write(toWrite)
    
    return path




#eof
