import SwiftUI
import AVFoundation

class CameraManager: NSObject, ObservableObject {
    @Published var session = AVCaptureSession()
    
    override init() {
        super.init()
        configureCamera()
    }
    
    func configureCamera() {
        session.sessionPreset = .high
        
        guard let device = AVCaptureDevice.default(.builtInWideAngleCamera, for: .video, position: .back) else {
            print("No camera available")
            return
        }
        
        do {
            let input = try AVCaptureDeviceInput(device: device)
            if session.canAddInput(input) {
                session.addInput(input)
            }
            
            let output = AVCaptureVideoDataOutput()
            if session.canAddOutput(output) {
                session.addOutput(output)
            }
            
            session.startRunning()
        } catch {
            print("Error setting up camera: \(error)")
        }
    }
}

struct CameraPreview: UIViewControllerRepresentable {
    @ObservedObject var cameraManager: CameraManager
    
    func makeUIViewController(context: Context) -> UIViewController {
        let controller = UIViewController()
        let previewLayer = AVCaptureVideoPreviewLayer(session: cameraManager.session)
        previewLayer.videoGravity = .resizeAspectFill
        previewLayer.frame = UIScreen.main.bounds
        controller.view.layer.addSublayer(previewLayer)
        return controller
    }
    
    func updateUIViewController(_ uiViewController: UIViewController, context: Context) {}
}
extension Color {
    init(hex: String) {
        let scanner = Scanner(string: hex)
        var rgb: UInt64 = 0
        scanner.scanHexInt64(&rgb)
        self.init(
            red: Double((rgb & 0xFF0000) >> 16) / 255.0,
            green: Double((rgb & 0x00FF00) >> 8) / 255.0,
            blue: Double(rgb & 0x0000FF) / 255.0
        )
    }
}
class ImageStack: ObservableObject {
    @Published var stack: [String] = []
    
    func addImageToStack(filename: String) {
        stack.append(filename)
    }
    
    func removeLastImage() -> String? {
        return stack.isEmpty ? nil : stack.removeLast()
    }
}

struct ContentView: View {
    @StateObject var stk = ImageStack()
    @State private var last: String?
    @State private var savedImages: [UIImage] = []
    
    func saveImage(image: UIImage) {
        if let imageData = image.pngData() {
            let manager = FileManager.default
            let documentsURL = manager.urls(for: .documentDirectory, in: .userDomainMask)[0]
            
            let fileName = UUID().uuidString + ".png"
            let fileURL = documentsURL.appendingPathComponent(fileName)
            
            do {
                try imageData.write(to: fileURL)
                stk.addImageToStack(filename: fileName)
                last = fileName
            } catch {
                print("Error saving image: \(error.localizedDescription)")
            }
        }
    }
    
    func loadLastImage() {
        guard let last = last else {
            let placeHolder = UIImage(named: "NoImages")
            savedImages.append(placeHolder!)
            return
        }
        
        let manager = FileManager.default
        let documentsURL = manager.urls(for: .documentDirectory, in: .userDomainMask)[0]
        let fileURL = documentsURL.appendingPathComponent(last)
        
        if let imageData = try? Data(contentsOf: fileURL), let image = UIImage(data: imageData) {
            savedImages.append(image)
        }
    }
    var body: some View {
        ZStack {
            VStack {
                Spacer()
                Rectangle()
                    .fill(Color(hex: "689df2"))
                    .frame(height: 155)
            }
            VStack {
                Rectangle()
                    .fill(Color(hex: "689df2"))
                    .frame(height: 160)
                    .edgesIgnoringSafeArea(.all)
                Spacer()
            }
            
            HStack {
                Image("FTCLogo")
                    .resizable()
                    .scaledToFit()
                    .frame(width: 150, height: 150)
                    .padding(.leading, -10)
                    .padding(.top, 690)
                Spacer()
            }
            HStack {
                Image("CaptureButton")
                    .resizable()
                    .scaledToFit()
                    .frame(width: 50, height: 50)
                    .padding(.top, 690)
            }
            
            HStack {
                if let lastImage = savedImages.last {
                    Image(uiImage: lastImage)
                        .resizable()
                        .scaledToFit()
                        .frame(width: 150, height: 150)
                        .border(Color.black, width: 4)
                } else {
                    Image("bear")
                        .resizable()
                        .frame(width: 80, height: 80)
                        .border(Color.black, width: 4)
                        .overlay(
                            Image("noName")
                                .resizable()
                                .scaledToFit()
                                .frame(width: 70, height: 50)
                                .rotationEffect(.degrees(-30))
                                .opacity(0.8)
                        )
                        .padding(.top, 700)
                        .padding(.leading, 280)
                }
            }
            .padding(.trailing, 20)
            .padding(.bottom, 20)
        }
    }
    
    
    struct ContentView_Previews: PreviewProvider {
        static var previews: some View {
            ContentView()
        }
    }
}
