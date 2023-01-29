
import { faCircleLeft, faCircleRight } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useEffect, useState } from "react";
import { MagnifyingGlass } from "react-loader-spinner";

export default function FirstPost() {
    const [currentIndex, setCurrentIndex] = useState(0);
    const [images, setImages] = useState([])
    const [types, setTypes] = useState([])
    const [alltypes, setAllTypes] = useState([])

    const handleNext = () => {
        setCurrentIndex(currentIndex === images.length - 1 ? 0 : currentIndex + 1);
        console.log(currentIndex);
    };

    const handlePrev = () => {
        setCurrentIndex(currentIndex === 0 ? images.length - 1 : currentIndex - 1);
        console.log(currentIndex);
        console.log(images[currentIndex]);
    };

    useEffect(() => {
    fetch('http://127.0.0.1:5001/model')
        .then((response) => response.json())
        .then((data) => {
            setImages(data.paths);
            setTypes(data.type);
            setAllTypes(data.typesall)
            console.log(data)
        })
        .catch((err) => {
            console.log(err.message);
        });
    }, []);

    return (
    <div> {images.length != 0 ? 
        <div className="flex-row bg-gradient-to-b from-cyan-500 to-blue-500 h-screen">
            <div className="text-3xl font-bold tracking-tight text-gray-900 border-b-2 border-gray-900 h-12 w-full pt-2 pl-4">
                Doctor Dashboard
            </div>
            <div className="text-black flex flex-row">
                <div className="pl-4 mt-6 text-xl">
                    Suspected Diagnosis: 
                </div>
                {types.map((type) => <div className={`t-6 text-xl px-2 ml-2 mt-6 rounded ${type!="Empty" ? "bg-red-400":"bg-green-400"}`}>
                    {type}
                </div>)}
            </div>
            <div className="text-black text-xl m-4 mt-6">
                We recommend you also take a look at these similar cases and their diagnoses:
            </div>
            <div className="flex flex-row justify-center mt-10 text-black">
                {currentIndex+1}/{images.length}
            </div>
            <div className="flex flex-row justify-center mt-5">
                <div className="h-96 flex mr-2 cursor-pointer" onClick={handlePrev}>
                    <FontAwesomeIcon icon={faCircleLeft} className="text-black self-center" size="2xl"/>
                </div>
                <div className="text-black w-96 h-96 rounded shadow-xl">
                    <img src={images[currentIndex]} alt="Image of Cancer" className="h-full w-full rounded-l-lg shadow-xl"/>
                </div>
                <div className="h-96 flex ml-2 cursor-pointer" onClick={handleNext}>
                    <FontAwesomeIcon icon={faCircleRight} className="text-black self-center" size="2xl"/>
                </div>
                <div className="text-gray-800 w-96 h-96 ml-20 rounded-lg shadow-xl backdrop-blur-lg bg-white/30">
                    <div className="w-full flex justify-center text-xl mt-4">
                        Radiologist Notes:
                    </div>
                    <div className="w-full text-xl mt-4 px-6">
                        Current image belongs to the <b>{alltypes[currentIndex]}</b> cluster
                        <div className="mt-3">
                        Extra notes:
                        <ul>
                            <li>- Discoloration near top right led to diagnosis</li>
                            <li>- Very confident in decision</li>
                            <li>- Discoloration near bottom is benign</li>
                        </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>:
        <div className="flex  bg-gradient-to-b from-cyan-500 to-blue-500 h-screen justify-center pt-80">
            <MagnifyingGlass
            visible={true}
            height="80"
            width="80"
            ariaLabel="MagnifyingGlass-loading"
            wrapperStyle={{}}
            wrapperClass="MagnifyingGlass-wrapper"
            glassColor = '#c0efff'
            color = '#e15b64'
            />
            <div className="text-gray-800 text-lg pt-4 font-bold">
                Finding closest matches...
            </div>
        </div>}
    </div>);
  }