import React from 'react';
import { useState } from 'react'
import Header from '../Header.jsx';
import Footer from '../Footer.jsx';

function Text_sheet(props) {
    return (
        <div className='py-4 px-10 bg-[#F65F6F] rounded-2xl text-white w-[90%] max-w-[600px] h-[600px] mx-auto'>
            <div className='flex flex-col h-full'>
                <div className='h-[15px]'></div>
                <div className='flex flex-col gap-[6px]'>
                    <h1 className='font-bold text-xl text-left'>ABOUT US</h1>
                    <p className='text-xl text-left'>We envision a future where NGOs and firms work hand in hand, leveraging each other’s strengths to tackle pressing issues such as poverty, education, health care, and environmental sustainability. Together, we can amplify our efforts, inspire others, and achieve sustainable solutions.</p>

                    <h1 className='font-bold text-xl text-left'>WHAT WE DO:</h1>

                    <p className='text-xl text-left'>Facilitate Connections: We provide a comprehensive database of NGOs and firms looking to collaborate.
                        We highlight successful partnerships and initiatives, showcasing how collaboration can lead to positive outcomes for society. </p>
                </div>
            </div>
        </div >
    )
}

function AboutUs() {
    return (
        <div className="min-h-screen flex flex-col">
            <Header />
            <div className="flex flex-col md:flex-row justify-center items-start gap-8 mx-auto py-10">
                <Text_sheet />
                {/* Раздел с Google Maps */}
                <div className="w-[90%] md:w-[600px] h-[400px] md:h-[600px]">
                    <iframe
                        title="Google Map Location"
                        src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d81348.06556296718!2d19.910661583725066!3d50.06008833051391!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x471644c0354e18d1%3A0xb46bb6b576478abf!2zS3Jha8Ozdw!5e1!3m2!1spl!2spl!4v1727590888344!5m2!1spl!2spl"
                        width="100%"
                        height="100%"
                        style={{ border: 0 }}
                        allowFullScreen=""
                        loading="lazy">
                    </iframe>
                </div>
            </div>
            <div className="flex-grow"></div>
            <Footer />
        </div>
    );
}
export default AboutUs;


