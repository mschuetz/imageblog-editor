#!/usr/bin/env python

import ibe
import sys
ibe.initialize_db()
if len(sys.argv) > 1 and sys.argv[1].lower() == 'debug':
    print >> sys.stderr, 'starting in debug mode'
    ibe.app.run(debug=True)
else:
    ibe.app.run(debug=False)
