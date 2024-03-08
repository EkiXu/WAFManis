// Require the framework and instantiate it
const fastify = require('fastify')({ logger: true })
const fs = require('fs')
const util = require('util')
const path = require('path')
const { pipeline } = require('stream')
const pump = util.promisify(pipeline)

fastify.register(require('@fastify/multipart'), { attachFieldsToBody: 'keyValues' })
fastify.register(require('@fastify/formbody'))

// Declare a route
fastify.post('/', async (request, reply) => {
  return { form : request.body }
})

// Run the server!
const start = async () => {
  try {
    await fastify.listen( 6000 , "0.0.0.0" )
  } catch (err) {
    fastify.log.error(err)
    process.exit(1)
  }
}
start()
