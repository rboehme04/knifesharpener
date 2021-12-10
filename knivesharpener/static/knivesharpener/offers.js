gsap.registerPlugin(ScrollTrigger);

gsap.defaults({
    duration: 1,
    opacity: 0,
});

gsap.from('#heading-1',{ 
    x: 25,
    scrollTrigger: '#header'
})

gsap.from('#image-1',{ 
    x: -25,
    scrollTrigger: '#header'
})

gsap.from('#heading-2',{ 
    x: -25,
    scrollTrigger: '#heading-1'
})

gsap.from('#image-2',{ 
    x: 25,
    scrollTrigger: '#heading-1'
})

gsap.from('#heading-3',{ 
    x: 25,
    scrollTrigger: '#heading-3'
})

gsap.from('#image-3',{ 
    x: -25,
    scrollTrigger: '#heading-3'
})

gsap.from('#heading-4',{ 
    x: -25,
    scrollTrigger: '#heading-4'
})

gsap.from('#image-4',{ 
    x: 25,
    scrollTrigger: '#heading-4'
})

