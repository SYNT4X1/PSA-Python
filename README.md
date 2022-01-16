<body>

  <p align="center">
    <img src="https://github.com/SyntaxError2435/imageSources/blob/main/PSA%20Header.png">
  </p>
  <h1 align="center">
    INTRODUCTION
  </h1>
    Hello world, how are you today? PSA, Polymorphic Subsitution Algorithm, is a python based encryption method made with the sole purpose of "polmorphising"
    the obfuscated data all whilst retaining identification through decryption. There has been a real time application of the encryption method using python
    sockets and a raspi, although for more general use cases, I would recommend down scaling the encryption method. Wait, Down scaling? Yes! PSA, is %100
    scalable in every sense of the word. So if you want more variance in the polymorphic obfuscation, simply add it, all with the assumption you have the
    resources to do so. One of the immediate drawbacks of PSA, is it's abundment amount of memory usage and data output, so if you plan to use it for any
    legitmate purposes, keep that in mind. 
  <h1 align="center">
    Rough Diagram of how it functions
  </h1>
  <p align="center">
    <img src="https://github.com/SyntaxError2435/imageSources/blob/main/PSA.png">
  </p>
  
  This illustrates that H is split from the main input and substituted from randomly selected and generated instances. This would be performed for each character     and then proceed to return the obfuscated data.
  
  <h1 align="center">
    Secure? How?
  </h1>
  
  PSA uses Blum Blum Shub for cryptographically secure rng, and generates possible seeds and modulus large prime numbers using mouse cursor input and system time   in 2 seperate slices of the time frame (however this may change since it's really slow). The generated possible primes are then tested by using a miller-rabin     primality test for 128 passes to try and "garuntee" a prime, well, garuntee enough for a 1024 - 2048 bit generated prime of course. PSA needs to be random since   it's entire process is based around generated randomnous, so by using CSPRNGs like Blum Blum Shub it should be of relative security to solving the quadratic       residuosity problem.
  
  <h1>
    FUTURE PLANS
  </h1>
  
  - make generation faster and optimize the encryption and decryption methods
  - implement server and client api 
  - implement rsa key exchange
  - implement key combination through xor operation or something similar
  
</body>
