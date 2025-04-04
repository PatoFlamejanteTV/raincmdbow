# raincmdbow 
Rainbow. Text.

## Args
```
parser.add_argument(
        "--delay", "-d", type=float, default=0.05,
        help="Delay between rows in seconds (default: 0.05)"
    )
    parser.add_argument(
        "--increment", "-i", type=float, default=0.1,
        help="Hue increment for each block (default: 0.1)"
    )
    parser.add_argument(
        "--char", "-c", type=str, default="█",
        help="Character to display (default: █)"
    )
    parser.add_argument(
        "--saturation", "-s", type=float, default=1.0,
        help="Color saturation, 0.0 to 1.0 (default: 1.0)"
    )
    parser.add_argument(
        "--brightness", "-b", type=float, default=1.0,
        help="Color brightness, 0.0 to 1.0 (default: 1.0)"
    )
    parser.add_argument(
        "--reverse", "-r", action="store_true",
        help="Reverse the rainbow direction"
    )
    parser.add_argument(
        "--pipe", "-p", action="store_true",
        help="Process piped input instead of generating rainbow screen"
    )
```
