from twisted.internet import ssl, reactor
from twisted.web.server import Site
from twisted.web.static import File

# Path to the self-signed certificate and private key files
certfile = "./certificate.pem"
keyfile = "./private.key"

# Create a Twisted web resource pointing to the directory you want to serve
resource = File("./")

# Create an SSL context and load the certificate and private key
ssl_context = ssl.DefaultOpenSSLContextFactory(keyfile, certfile)

# Create a Twisted web server site with the SSL context and the resource
site = Site(resource, contextFactory=ssl_context)

# Set the listening port and start the Twisted reactor
reactor.listenSSL(8443, site, ssl_context)
reactor.run()
