const NodeRSA = require('node-rsa');
const uuid = require('uuid');

this.KEY = new NodeRSA({b: 512});
this.KEY.generateKeyPair();
this.PUBLIC_KEY = this.KEY.exportKey('public')
this.PRIVATE_KEY = this.KEY.exportKey('private')
console.log("pub", this.PUBLIC_KEY)
console.log("priv", this.PRIVATE_KEY)
this.KEY_COMP = this.KEY.exportKey('components-public');
console.log("n", this.KEY_COMP.n.toString('base64'))
this.KID = uuid.v4();
console.log("kid", this.KID)

