import React from "react";
import Slider from "react-slick";
import "./Carousel.css";

const newsArticles = [
    { imageUrl: "/src/assets/caritas.png" },
    { imageUrl: "/src/assets/siepomaga.jpg" },
    { imageUrl: "/src/assets/fundacja-polsat-ikona.png" },
    { imageUrl: "/src/assets/pck.jpg" },
    { imageUrl: "/src/assets/wosp.png" },
];

const Carousel = () => {
    const settings = {
        centerMode: true,
        centerPadding: "0",
        slidesToShow: 3,
        infinite: true,
        speed: 500,
        autoplay: true,
        autoplaySpeed: 3000,
        focusOnSelect: true,
        responsive: [
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 1,
                },
            },
        ],
    };

    return (
        <div className="carousel-container">
            <Slider {...settings}>
                {newsArticles.map((article, index) => (

                    <div key={index} className="carousel-slide">
                        <img
                            src={article.imageUrl}
                            className="carousel-image"
                        />
                        <div className="carousel-content">
                        </div>
                    </div>
                ))}
            </Slider>
        </div>
    );
};

export default Carousel;
